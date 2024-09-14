from typing import Any

from clean_data import ForecastDataCleaners
from display_data import ForecastDataDisplayer
from get_data import ForecastDataGetter


def main() -> None:
    """Call to print daily forecasts."""
    weather_data_raw: list[dict[str, Any]] = ForecastDataGetter().weather_data_raw
    clean_data: list[dict[str, Any]] = ForecastDataCleaners(
        forecast=weather_data_raw
    ).clean_data
    displayer = ForecastDataDisplayer(clean_forecast=clean_data)
    displayer.print_daily_forecasts()

if __name__ == "__main__":
    main()
