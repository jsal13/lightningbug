import os
from typing import Any

import attrs
import pandas as pd
import tabulate

tabulate.WIDE_CHARS_MODE = True

@attrs.define
class ForecastDataDisplayer:
    """Pretty print the daily forecasts."""

    clean_forecast: list[dict[str, Any]]
    daily_forecast_list: list[tuple[str, pd.DataFrame]] = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:
        self.daily_forecast_list = self._create_daily_dfs()

    def _create_daily_dfs(self) -> list[tuple[str, pd.DataFrame]]:
        """Create a list of dataframes grouped by date."""
        df_forecast = pd.DataFrame(self.clean_forecast)
        keys = df_forecast["date"].unique()

        df_groups = []
        for key in keys:
            _df = df_forecast[df_forecast["date"] == key]
            _df_slimmed = _df.drop("date", axis=1)
            df_groups.append((key, _df_slimmed))

        return df_groups

    def create_tables_forecast(self) -> list[tuple[str, str]]:
        """Create a table forecast to print."""
        dfs_str = []

        for _df in self.daily_forecast_list:
            date_val, df_forecast = _df

            # time, temp, humid, wind, forecast
            colalign = ("right", "right", "right", "right", "left")
            df_str = tabulate.tabulate(
                df_forecast,  # type: ignore
                showindex=False,
                headers=df_forecast.columns.to_list(),
                tablefmt="fancy_outline",
                colalign=colalign,
            )
            dfs_str.append((date_val, df_str))
        return dfs_str

    def print_daily_forecasts(self) -> None:
        """Pretty print the daily forecasts."""

        def _clear_screen() -> None:
            """Clear the screen on the terminal."""
            clear_cmd = "cls" if os.name == "nt" else "clear"
            os.system(clear_cmd)

        _clear_screen()

        dfs_str = self.create_tables_forecast()
        for df_str in dfs_str:
            print(df_str[0], df_str[1], sep="\n", end="\n\n")
