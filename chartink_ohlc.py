# filename: chartink_ohlc.py

# line 1
import requests
import pandas as pd
from datetime import datetime

# line 3
session = requests.Session()

"""
requests.Session() creates a persistent session in Python Requests, 
enabling cookie storage, connection reuse, and shared settings like headers or authentication 
across multiple HTTP requests. This improves performance and maintains state, 
making it ideal for web scraping and API interactions.
"""
# line 5
url = "https://chartink.com/oapi"

# line 7
headers = {
# line 8
    "x-requested-with": "XMLHttpRequest",
# line 9
    "referer": "https://chartink.com/stocks-new?symbol=HDFCGOLD",
# line 10
    "user-agent": (
# line 11
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
# line 12
        "AppleWebKit/537.36 (KHTML, like Gecko) "
# line 13
        "Chrome/148.0.0.0 Safari/537.36"
# line 14
    )
# line 15
}

# line 5
start_date = "2025-01-01"

# line 6
end_date = "2025-01-10"

# line 7
timeframe_minutes = 30

# line 9
start_dt = datetime.strptime(start_date, "%Y-%m-%d")

# line 10
end_dt = datetime.strptime(end_date, "%Y-%m-%d")

# line 12
days = (end_dt - start_dt).days

# line 14
candles_per_day = (24 * 60) // timeframe_minutes

# line 16
size = days * candles_per_day

# line 18
end_time_ms = int(end_dt.timestamp() * 1000)

# line 20
payload = {
# line 21
    "query": (
# line 22
        "select open, high, low, close, volume "
# line 23
        "where symbol='HDFCGOLD'"
# line 24
    ),
# line 25
    "use_live": 1,
# line 26
    "limit": 1,
# line 27
    "size": size,
# line 28
    "widget_id": -1,
# line 29
    "end_time": end_time_ms,
# line 30
    "timeframe": "30 minutes",
# line 31
    "symbol": "HDFCGOLD",
# line 32
    "scan_link": "null"
# line 33
}

# line 35
response = requests.post(
# line 36
    "https://chartink.com/oapi",
# line 37
    data=payload,
# line 38
headers=headers
)

# line 40
data = response.json()

# filename: chartink_ohlc.py

# line 100
results = data["groupData"][0]["results"]

# line 102
opens = results[0]["open"]

# line 103
highs = results[1]["high"]

# line 104
lows = results[2]["low"]

# line 105
closes = results[3]["close"]

# line 106
volumes = results[4]["volume"]

# line 108
df = pd.DataFrame({
# line 109
    "Open": opens,
# line 110
    "High": highs,
# line 111
    "Low": lows,
# line 112
    "Close": closes,
# line 113
    "Volume": volumes
# line 114
})

# line 116
df.replace(1.7e308, pd.NA, inplace=True)

# line 118
df.dropna(inplace=True)

# line 120
df.reset_index(drop=True, inplace=True)

# line 122
end_datetime = pd.to_datetime(
# line 123
    end_time_ms,
# line 124
    unit="ms"
# line 125
)

# line 127
df["Datetime"] = pd.date_range(
# line 128
    end=end_datetime,
# line 129
    periods=len(df),
# line 130
    freq="30min"
# line 131
)

# line 133
df = df[
# line 134
    [
# line 135
        "Datetime",
# line 136
        "Open",
# line 137
        "High",
# line 138
        "Low",
# line 139
        "Close",
# line 140
        "Volume"
# line 141
    ]
# line 142
]

# line 144
print(df.head())

# line 145
print(df.tail())