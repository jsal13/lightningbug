from collections import OrderedDict

KEYWORDS_TO_SYMBOLS_LIST = [
    ["smoke", "🔥"],
    ["rain", "🌧️"],
    ["partly sunny", "🌥️"],
    ["partly cloudy", "⛅"],
    ["sunny", "☀️"],
    ["cloudy", "☁️"],
    ["clear", "🟦"],
]


FORECAST_SYMBOL_MAP: dict[str, str] = OrderedDict(KEYWORDS_TO_SYMBOLS_LIST)


DIRECTION_SYMBOL_MAP = {
    "N": "↑",
    "NNE": "↗",
    "NE": "↗",
    "ENE": "↗",
    "E": "→",
    "ESE": "↘",
    "SE": "↘",
    "SSE": "↘",
    "S": "↓",
    "SSW": "↙",
    "SW": "↙",
    "WSW": "↙",
    "W": "←",
    "WNW": "↖",
    "NW": "↖",
    "NNW": "↖",
}

MIN_VERY_HOT_TEMP = 80
MAX_VERY_COLD_TEMP = 0
MIN_VERY_WINDY_TEMP = 20
