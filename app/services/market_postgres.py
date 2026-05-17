
import pandas as pd
import sqlalchemy
from Credentials.credentials import Cred

engine = sqlalchemy.create_engine(
    f'postgresql+psycopg2://{Cred.username}:{Cred.pwd}@{Cred.hostname}:{Cred.port_id}/{Cred.database}'
)
def save_ohlc_data(
    df: pd.DataFrame,
    token: int,
    symbol: str,
    timeframe: str
):

    df = df.copy()

    df.rename(
        columns={
            "Datetime": "datetime",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        },
        inplace=True
    )
    
    df["token"] = token

    df["symbol"] = symbol
    df["timeframe"] = timeframe
    df = df[
        [
            "token",
            "symbol",
            "timeframe",
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume"
        ]
    ]

    df.to_sql(
        name="market_data",
        con=engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print(f"{symbol} inserted successfully")