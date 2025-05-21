import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

INPUT_PATH = "input/test.csv"
OUTPUT_PATH = "output/prediction.csv"

os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Считываем входной CSV
df = pd.read_csv(INPUT_PATH)
df["time"] = pd.to_datetime(df["time"])

# Список для всех строк предсказания
all_predictions = []

for _, row in df.iterrows():
    station = row["station"]
    base_time = row["time"]

    for i in range(24):
        forecast_time = base_time + timedelta(hours=i)

        # Генерация фейковых предсказаний
        temperature = round(np.random.uniform(0, 20), 2)
        pressure = round(np.random.uniform(740, 770), 2)
        humidity = round(np.random.uniform(30, 90), 2)
        wind_speed = round(np.random.uniform(0, 10), 2)
        wind_direction = int(np.random.uniform(0, 360))

        all_predictions.append({
            "station": station,
            "time": forecast_time.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humidity,
            "wind speed": wind_speed,
            "wind direction": wind_direction
        })

# Сохранение в prediction.csv
output_df = pd.DataFrame(all_predictions)
output_df.to_csv(OUTPUT_PATH, index=False)

