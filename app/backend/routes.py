from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
import pandas as pd
from .schemas import PredictRequest, WeatherData
import io
import os

router = APIRouter(
    prefix="/api",
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
    
# 7 input
@router.post("/predict")
async def predict(request: PredictRequest):
    station = request.station
    time = request.time

    # ТУТ МОДЕЛЬ СОЗДАЕТ csv

    # Загружаем предсказания из файла
    prediction_path = "backend/output/prediction.csv"
    if not os.path.exists(prediction_path):
        return JSONResponse(status_code=500, content={"error": "Prediction file not found"})

    pred_df = pd.read_csv(prediction_path)

    # Фильтруем предсказания по station и time (time — начальное время)
    # Предполагается, что prediction.csv содержит 24 часа вперед для каждой пары station + time

    # Группировка по station и time
    result = []
    grouped = pred_df.groupby(["station", "time"])  # maybe delete

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
async def predict_with_full(request: WeatherData):
    station = request.station
    time = request.time
    temperature = request.temperature
    pressure = request.pressure
    humidity = request.humidity
    wind_speed = request.wind_speed
    wind_direction = request.wind_direction

    # ТУТ МОДЕЛЬ СОЗДАЕТ csv

    # Загружаем предсказания из файла
    prediction_path = "backend/output/prediction.csv"
    if not os.path.exists(prediction_path):
        return JSONResponse(status_code=500, content={"error": "Prediction file not found"})

    pred_df = pd.read_csv(prediction_path)

    # Фильтруем предсказания по station и time (time — начальное время)
    # Предполагается, что prediction.csv содержит 24 часа вперед для каждой пары station + time

    # Группировка по station и time
    result = []
    grouped = pred_df.groupby(["station", "time"])  # maybe delete

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

@router.get("/index", response_class=HTMLResponse)
async def get_index():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)