import csv
# import json
from datetime import datetime, timezone
from pathlib import Path

import httpx
import asyncio

BASE_DIR = Path(__file__).resolve().parent.parent
async def fetch_data():
    url = "https://sset.envdigital.mts.ru/api/v1/chart/data?form_data=%7B%22slice_id%22%3A84%7D&dashboard_id=63&force=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
        "Accept": "application/json",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "X-CSRFToken": "IjJkNjVlZDM2ZDU4NDBlNGVhNjYzZDNlYzFlZWI1NDlmNTI4MmY1NDUi.aC1dXw.mlOGr0WG1eT4XQtY38zyd35G7LU",
        "Content-Type": "application/json",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "same-origin",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }
    body = {
        "datasource": {"id": 90, "type": "table"},
        "force": True,
        "queries": [
            {
                "time_range": 'DATEADD(DATETIME("now"), -24, hour) : now',
                "filters": [{"col": "time", "op": "TEMPORAL_RANGE", "val": "No filter"}],
                "extras": {"having": "", "where": ""},
                "applied_time_extras": {},
                "columns": [
                    "station", "time", "NO2", "O3", "H2S", "CO", "SO2",
                    "Температура, °С", "davlenie", "vlazhnost",
                    "Скорость ветра, м/с", "Направление ветра, °"
                ],
                "orderby": [],
                "annotation_layers": [],
                "row_limit": 50000,
                "series_limit": 0,
                "order_desc": True,
                "url_params": {},
                "custom_params": {},
                "custom_form_data": {},
                "post_processing": [],
                "time_offsets": []
            }
        ],
        "form_data": {
            "datasource": "90__table",
            "viz_type": "table",
            "slice_id": 84,
            "url_params": {},
            "query_mode": "raw",
            "groupby": [],
            "temporal_columns_lookup": {"time": True},
            "all_columns": [
                "station", "time", "NO2", "O3", "H2S", "CO", "SO2",
                "Температура, °С", "davlenie", "vlazhnost",
                "Скорость ветра, м/с", "Направление ветра, °"
            ],
            "percent_metrics": [],
            "adhoc_filters": [
                {"clause": "WHERE", "comparator": "No filter", "expressionType": "SIMPLE",
                 "operator": "TEMPORAL_RANGE", "subject": "time"}
            ],
            "order_by_cols": [],
            "row_limit": 50000,
            "server_page_length": 10,
            "order_desc": True,
            "table_timestamp_format": "smart_date",
            "allow_render_html": True,
            "show_cell_bars": False,
            "color_pn": False,
            "comparison_color_scheme": "Green",
            "conditional_formatting": [],
            "comparison_type": "values",
            "dashboards": [63],
            "extra_form_data": {"time_range": 'DATEADD(DATETIME("now"), -24, hour) : now'},
            "label_colors": {},
            "shared_label_colors": {},
            "extra_filters": [],
            "dashboardId": 63,
            "force": True,
            "result_format": "json",
            "result_type": "full",
            "include_time": False
        },
        "result_format": "json",
        "result_type": "full"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        response.raise_for_status()  # Если нужен выброс исключения при ошибке
        data = response.json()
        return data

# Запуск
async def get_data_parse():
    result = await fetch_data()
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