import csv
# import json
from datetime import datetime, timezone
from pathlib import Path

import requests_cache
import requests

# Установка кэша на 1 час
requests_cache.install_cache(
    'http_cache',
    expire_after=600,
    allowable_methods=('GET', 'POST')
)

BASE_DIR = Path(__file__).resolve().parent.parent
def fetch_data():

    response = requests.post(url, headers=headers, json=body)
    print(response.from_cache) 
    data = response.json()
    return data
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(url, headers=headers, json=body)
    #     response.raise_for_status()  # Если нужен выброс исключения при ошибке
    #     data = response.json()
    #     return data

# Запуск
def get_data_parse():
    result = fetch_data()
    # with open("result.json", "w", encoding="utf-8") as f:
    #     json.dump(result, f, ensure_ascii=False, indent=4)
    #
    # with open("result.json", "r", encoding="utf-8") as f:
    #     result = json.load(f)

    # print(json.dumps(result['result'][0]['data'], indent=4, ensure_ascii=False))
    result = result['result'][0]['data']

    with open(BASE_DIR / "backend"/ "output" / "output.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Заголовок
        writer.writerow([
            "Пост мониторинга", "Период", "NO2", "O3", "H2S", "CO", "SO2",
            "Температура, °С", "Давление, мм рт. ст.", "Влажность, %",
            "Скорость ветра, м/с", "Направление ветра, °"
        ])
        # Данные
        for row in result:
            time_str = datetime.fromtimestamp(row["time"] / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([
                row["station"], time_str, row["NO2"], row["O3"], row["H2S"], row["CO"],
                row["SO2"], row["Температура, °С"], row["davlenie"], row["vlazhnost"],
                row["Скорость ветра, м/с"], row["Направление ветра, °"]
            ])

if __name__ == "__main__":
    get_data_parse()
    get_data_parse()
    get_data_parse()
