from datetime import datetime
from typing import Any

import attrs
from constants import (
    DIRECTION_SYMBOL_MAP,
    FORECAST_SYMBOL_MAP,
    MAX_VERY_COLD_TEMP,
    MIN_VERY_HOT_TEMP,
    MIN_VERY_WINDY_TEMP,
)


@attrs.define
class ForecastDataCleaners:
    """
    Clean up data to make it look nice.

    Each row in `data` should look like:
    {
        'startTime': '2023-06-28T23:00:00-05:00',
        'temperature': 67,
        'temperatureUnit': 'F',
        'probabilityOfPrecipitation': 31,
        'relativeHumidity': 75,
        'windSpeed': '5 mph',
        'windDirection': 'SE',
        'shortForecast': 'Chance Showers And Thunderstorms'
    }
    """

    forecast: list[dict[str, Any]]
    clean_data: list[dict[str, Any]] = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:
        self.clean_data = []
        for row in self.forecast:
            date, time = ForecastDataCleaners.format_datetime(row["startTime"])
            temperature = ForecastDataCleaners.format_temperature(
                temp=row["temperature"],
                temp_unit=row["temperatureUnit"],
            )
            humidity = ForecastDataCleaners.format_humidity(
                humidity=row["relativeHumidity"],
            )
            wind = ForecastDataCleaners.format_wind(
                wind_speed=row["windSpeed"],
                wind_dir=row["windDirection"],
            )

            short_forecast = ForecastDataCleaners.format_short_forecast(
                short_forecast=str(row.get("shortForecast"))
            )

            formatted_row = {
                "date": date,
                "time": time,
                "temp": temperature,
                "humid": humidity,
                "wind": wind,
                "forecast": short_forecast,
            }
            self.clean_data.append(formatted_row)

    @staticmethod
    def format_datetime(val: str) -> tuple[str, str]:
        """
        Format piped-in datetime to a pretty format.

        Input value is like this:
        "2023-06-28T15:00:00-05:00"
        """
        _dt = datetime.strptime(val, "%Y-%m-%dT%H:%M:%S%z")

        date = datetime.strftime(_dt, "%a, %b %d")
        time = datetime.strftime(_dt, "%-I %p")
        return date, time

    @staticmethod
    def format_temperature(temp: int, temp_unit: str) -> str:
        """Format temp to a pretty format."""
        temp_str: str = ""
        if temp >= MIN_VERY_HOT_TEMP:
            temp_str = "🌡️ "
        elif temp <= MAX_VERY_COLD_TEMP:
            temp_str = "❄️ "

        temp_str += f"{temp}°{temp_unit}"

        return temp_str

    @staticmethod
    def format_humidity(humidity: int) -> str:
        """Format humidity to a pretty format."""
        return f"{humidity}%"

    @staticmethod
    def format_wind(wind_speed: str, wind_dir: str) -> str:
        """Format wind to a pretty format."""
        wind_speed, wind_speed_dims = wind_speed.split(" ")

        wind_str: str = ""
        if int(wind_speed) >= MIN_VERY_WINDY_TEMP:
            wind_str = "💨 "

        wind_dir_symbol = DIRECTION_SYMBOL_MAP.get(wind_dir, wind_dir)
        wind_str += f"{wind_speed} {wind_speed_dims} {wind_dir_symbol}"
        return wind_str

    @staticmethod
    def format_short_forecast(short_forecast: str) -> str:
        """Format short_forecast to a pretty format."""
        short_forecast_lower = short_forecast.lower()
        short_forecast_str: str = ""
        for key, symbol in FORECAST_SYMBOL_MAP.items():
            if key in short_forecast_lower:
                short_forecast_str = symbol + " "
                break

        short_forecast_str += f"{short_forecast}"
        return short_forecast_str
