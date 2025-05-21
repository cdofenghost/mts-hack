from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    station: str
    time: str  # ISO формат времени, например "2025-04-28 18:20:00"

class WeatherData(BaseModel):
    station: str
    time: str
    temperature: float = Field(..., alias="temperature")
    pressure: float
    humidity: float
    wind_speed: float = Field(..., alias="wind speed")
    wind_direction: float = Field(..., alias="wind direction")