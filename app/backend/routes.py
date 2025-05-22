from pathlib import Path

from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
import pandas as pd
from .schemas import PredictRequest, WeatherData
from .parser import get_data_parse
import io
import os
from app.ml.ml import analyze

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
BACKEND_DIR = BASE_DIR / "backend"

router = APIRouter(
    tags=["API"])

@router.get("/download_csv")
async def download_csv() -> FileResponse:
    # Загружаем предсказания из файла
    prediction_path = BACKEND_DIR / "prediction.csv"
    if not os.path.exists(prediction_path):
        return JSONResponse(status_code=500, content={"error": "Prediction file not found"})

    return FileResponse(path=prediction_path, filename="prediction.csv")


@router.post("/predict_with_full")
def predict_with_full():
    get_data_parse()
    analyze(BASE_DIR / "backend" / "output" / "output.csv")
    # Загружаем предсказания из файла
    prediction_path = BACKEND_DIR / "prediction.csv"
    if not os.path.exists(prediction_path):
        return JSONResponse(status_code=500, content={"error": "Prediction file not found"})

    pred_df = pd.read_csv(prediction_path)

    column_mapping = {
        "Температура, °С": "temperature",
        "Давление, мм рт. ст.": "pressure",
        "Влажность, %": "humidity",
        "Скорость ветра, м/с": "wind_speed",
        "Направление ветра, °": "wind_direction"
    }
    columns = list(column_mapping.keys())
    result = []
    for _, row in pred_df.iterrows():
        entry = {column_mapping[col]: row[col] for col in columns}
        result.append(entry)

    return {"predictions": result}

@router.get("/index", response_class=HTMLResponse)
async def get_index():
    return FileResponse(FRONTEND_DIR / "index.html")
