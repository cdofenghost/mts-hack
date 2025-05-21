from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    station: str
    time: str  # ISO формат времени, например "2025-04-28 18:20:00"

class WeatherData(BaseModel):
    station: str = Field(..., alias="Пост мониторинга")
    no2: float = Field(..., alias="NO2")
    o3: float = Field(..., alias="O3")
    h2s: float = Field(..., alias="H2S")
    co: float = Field(..., alias="CO")
    so2: float = Field(..., alias="SO2")
    temperature: float = Field(..., alias="Температура, °С")
    pressure: float = Field(..., alias="Давление, мм рт. ст.")
    humidity: float = Field(..., alias="Влажность, %")
    wind_speed: float = Field(..., alias="Скорость ветра, м/с")
    wind_direction: float = Field(..., alias="Направление ветра, °")
    year: int = Field(..., alias="Год")
    month: int = Field(..., alias="Месяц")
    hour: int = Field(..., alias="Час")
    minute: int = Field(..., alias="Минута")