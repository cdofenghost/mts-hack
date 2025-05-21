from pathlib import Path

from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
import pandas as pd
from .schemas import PredictRequest, WeatherData
from .parser import get_data_parse
import io
import os

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
BACKEND_DIR = BASE_DIR / "backend"

router = APIRouter(
    tags=["API"])

# only station+time
@router.post("/predict_from_csv")
async def predict_from_csv(file: UploadFile = File(...)):
    # Считать CSV из запроса
    contents = await file.read()
    test_df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    # ТУТ МОДЕЛЬ СОЗДАЕТ csv

    # Сохранить файл, чтобы передать ML-команде (если надо)
    test_df.to_csv("backend/input/test.csv", index=False)

    # Предполагаем, что ML-команда возвращает prediction.csv в формате:
    # station,time,temperature,pressure,humidity,wind speed,wind direction
    prediction_path = "./output/prediction.csv"
    if not os.path.exists(prediction_path):
        return JSONResponse(status_code=500, content={"error": "Prediction file not found"})

    pred_df = pd.read_csv(prediction_path)

    # Группировка по station и time
    result = []
    grouped = pred_df.groupby(["station", "time"]) # maybe delete

    for (station, start_time), group in grouped:
        rows = group.reset_index(drop=True)

        result.append({
            "station": station,
            "time": start_time,
            "temperature": rows["temperature"].tolist(),
            "pressure": rows["pressure"].tolist(),
            "humidity": rows["humidity"].tolist(),
            "wind_speed": rows["wind speed"].tolist(),
            "wind_direction": rows["wind direction"].tolist(),
        })

    return {"predictions": result}

# full weather data
@router.post("/predict_with_full")
async def predict_with_full():
    await get_data_parse()

    # ТУТ МОДЕЛЬ СОЗДАЕТ csv

    # Загружаем предсказания из файла
    prediction_path = BACKEND_DIR / "output" / "output.csv"
    if not os.path.exists(prediction_path):
        return JSONResponse(status_code=500, content={"error": "Prediction file not found"})

    pred_df = pd.read_csv(prediction_path)

    columns = [
        "NO2",
        "O3",
        "H2S",
        "CO",
        "SO2",
        "Температура, °С",
        "Давление, мм рт. ст.",
        "Влажность, %",
        "Скорость ветра, м/с",
        "Направление ветра, °"
    ]
    # Группировка по station и time
    result = []
    for _, row in pred_df.iterrows():
        entry = {col: row[col] for col in columns}
        result.append(entry)

    return {"predictions": result}

@router.get("/index", response_class=HTMLResponse)
async def get_index():
    return FileResponse(FRONTEND_DIR / "index.html")
