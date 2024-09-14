from typing import Any

import attrs
import requests


@attrs.define
class ForecastDataGetter:
    """Get forecast data for given ``lat`` and ``lng``."""

    lat: float = attrs.field(default=41.9328)
    lng: float = attrs.field(default=-87.6427)
    station_data: dict[str, Any] = attrs.field(init=False)
    weather_data_raw: list[dict[str, Any]] = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:
        self.station_data: dict[str, Any] = self._get_closest_station()
        self.weather_data_raw = self._get_18_hours_of_forecast_data()

    def _get_closest_station(self) -> dict[str, Any]:
        """Return closest weather station to ``lat`` and ``lng`` (Default: Chicago)."""
        resp = requests.get(
            f"https://api.weather.gov/points/{self.lat},{self.lng}", timeout=60
        )
        data = resp.json().get("properties")

        station_data = {
            "cwa": data.get("cwa"),
            "gridX": data.get("gridX"),
            "gridY": data.get("gridY"),
        }
        return station_data

    def _get_18_hours_of_forecast_data(self) -> list[dict[str, Any]]:
        """Get 18 hours of forecast data from given ``station_data``."""
        url = (
            "https://api.weather.gov/gridpoints/"
            + f"{self.station_data['cwa']}/"
            + f"{self.station_data['gridX']},{self.station_data['gridX']}"
            + "/forecast/hourly"
            + "?units=us"
        )
        resp = requests.get(url, timeout=60).json().get("properties").get("periods")
        resp_first_18 = resp[:18]

        data = [
            {
                "startTime": row.get("startTime"),
                "temperature": row.get("temperature"),
                "temperatureUnit": row.get("temperatureUnit"),
                "probabilityOfPrecipitation": row.get("probabilityOfPrecipitation").get(
                    "value"
                ),
                "relativeHumidity": row.get("relativeHumidity").get("value"),
                "windSpeed": row.get("windSpeed"),
                "windDirection": row.get("windDirection"),
                "shortForecast": row.get("shortForecast"),
            }
            for row in resp_first_18
        ]

        return data
