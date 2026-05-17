# filename: C:\Users\Arpit\Desktop\NSE_DATA\app\services\NSE_Charting.py


import requests


import pandas as pd


session = requests.Session()


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/148.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://charting.nseindia.com/",
    "Origin": "https://charting.nseindia.com"
}



session.get(
    "https://charting.nseindia.com/",
    headers=HEADERS
)



def get_ohlc(
    token: int,
    symbol: str,
    from_date: int,
    to_date: int,
    time_interval: int = 5,
    chart_type: str="I",
    symbol_type: str = "Equity"
) -> pd.DataFrame:

    nse_url = (
        "https://charting.nseindia.com/v1/charts/"
        "symbolHistoricalData"
        f"?token={token}"
        f"&fromDate={from_date}"
        f"&toDate={to_date}"
        f"&symbol={symbol}"
        f"&symbolType={symbol_type}"
        f"&chartType={chart_type}"
        f"&timeInterval={time_interval}"
    )

    print(nse_url)

    response = session.get(
        nse_url,
        headers=HEADERS
    )


  
    if response.status_code != 200:
        raise Exception(
            f"NSE request failed: {response.status_code}"
        )



    data = response.json()


    if not data:
        raise Exception(
            "NSE returned no candle data"
        )

    

    df = pd.DataFrame(data["data"])


    df.rename(
        columns={
            "time": "Datetime",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume"
        },
        inplace=True
    )



    df["Datetime"] = pd.to_datetime(
        df["Datetime"],
        unit="ms"
    )



    df = df[
        [
            "Datetime",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]
    ]


  
    return df

get_ohlc(4963,"ICICIBANK-EQ",1746075900,1746698400,1,"D","Equity")