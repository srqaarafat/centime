class AlphaVantageConstants:
    intra_day_function = "TIME_SERIES_INTRADAY"
    intra_day_extended_function = "TIME_SERIES_INTRADAY_EXTENDED"
    daily_function = "TIME_SERIES_DAILY"
    daily_adjusted_function = "TIME_SERIES_DAILY_ADJUSTED"
    weekly_function = "TIME_SERIES_WEEKLY"
    weekly_Adjusted_function = "TIME_SERIES_WEEKLY_ADJUSTED"
    monthly_function = "TIME_SERIES_MONTHLY"
    monthly_adjusted_function = "TIME_SERIES_MONTHLY_ADJUSTED"
    min_interval = lambda minute: "{}min".format(minute)
    slice_year_month = lambda yr, mh: "year{}month{}".format(yr, mh)

    meta_deta_schema = {
        "type": "object",
        "properties": {
            "Meta Data": {"type": "object"},
            "properties": {
                "1. Information": {"type": "string"},
                "2. Symbol": {"type": "string"},
                "3. Last Refreshed": {"type": "string"},
                "4. Interval": {"type": "string"},
                "5. Output Size": {"type": "string"},
                "6. Time Zone": {"type": "string"}
            }
        },
        "required": ["Meta Data"]
    }

    time_series_schema = {
        "type": "object",
        "properties": {
            "1. open": {"type": "string"},
            "2. high": {"type": "string"},
            "3. low": {"type": "string"},
            "4. close": {"type": "string"},
            "5. volume": {"type": "string"},
        },
        "required": ["1. open", "2. high", "3. low", "4. close", "5. volume"]
    }

    daily_series_adjusted_schema = {
        "type": "object",
        "properties": {
            "Information": {"type": "string"},
            },
        "required": ["Information"]
    }

    weekly_adjusted_time_series_schema = {
        "type": "object",
        "properties": {
            "1. open": {"type": "string"},
            "2. high": {"type": "string"},
            "3. low": {"type": "string"},
            "4. close": {"type": "string"},
            "5. adjusted close": {"type": "string"},
            "6. volume": {"type": "string"},
            "7. dividend amount": {"type": "string"},
        },
        "required": ["1. open", "2. high", "3. low", "4. close", "5. adjusted close", "6. volume", "7. dividend amount"]
    }