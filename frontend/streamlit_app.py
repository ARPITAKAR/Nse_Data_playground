# filename: frontend/streamlit_app.py

import streamlit as st

# line 2
import requests

# line 3
import pandas as pd

# line 4
from datetime import datetime, timedelta


# line 7
FASTAPI_URL = "http://127.0.0.1:8000/download"


# line 10
st.set_page_config(
# line 11
    page_title="NSE Data Downloader",
# line 12
    layout="wide"
# line 13
)


# line 16
st.title("NSE Historical Data Downloader")

# line 17
st.markdown(
# line 18
    "Download OHLC market data from NSE backend API"
# line 19
)


# line 22
with st.sidebar:

    # line 24
    st.header("Market Parameters")

    # line 26
    trade_name = st.text_input(
    # line 27
        label="Trading Symbol",
    # line 28
        value="ICICIBANK-EQ"
    # line 29
    )

    # line 31
    token = st.number_input(
    # line 32
        label="Token",
    # line 33
        value=4963,
    # line 34
        step=1
    # line 35
    )

    # line 37
    symbol_type = st.selectbox(
    # line 38
        label="Symbol Type",
    # line 39
        options=[
    # line 40
            "Equity",
    # line 41
            "Futures",
    # line 42
            "Options"
    # line 43
        ]
    # line 44
    )

    # line 46
    chart_type = st.selectbox(
    # line 47
        label="Chart Type",
    # line 48
        options=[
    # line 49
            "I",
    # line 50
            "D",
    # line 51
            "W",
    # line 52
            "M"
    # line 53
        ]
    # line 54
    )

    # line 56
    time_interval = st.selectbox(
    # line 57
        label="Time Interval",
    # line 58
        options=[1, 5, 15, 30, 60],
    # line 59
        index=0
    # line 60
    )


# line 64
st.subheader("Date Range")


# line 67
col1, col2 = st.columns(2)


# line 70
with col1:

    # line 72
    from_date = st.date_input(
    # line 73
        label="From Date",
    # line 74
        value=datetime.now() - timedelta(days=30)
    # line 75
    )

    # line 77
    from_time = st.time_input(
    # line 78
        label="From Time",
    # line 79
        value=datetime.strptime(
    # line 80
            "09:15",
    # line 81
            "%H:%M"
    # line 82
        ).time()
    # line 83
    )


# line 87
with col2:

    # line 89
    to_date = st.date_input(
    # line 90
        label="To Date",
    # line 91
        value=datetime.now()
    # line 92
    )

    # line 94
    to_time = st.time_input(
    # line 95
        label="To Time",
    # line 96
        value=datetime.strptime(
    # line 97
            "15:30",
    # line 98
            "%H:%M"
    # line 99
        ).time()
    # line 100
    )


# line 104
from_datetime = datetime.combine(
# line 105
    from_date,
# line 106
    from_time
# line 107
)


# line 110
to_datetime = datetime.combine(
# line 111
    to_date,
# line 112
    to_time
# line 113
)


# line 116
payload = {
# line 117
    "trade_name": trade_name,
# line 118
    "token": int(token),
# line 119
    "from_date": from_datetime.isoformat(),
# line 120
    "to_date": to_datetime.isoformat(),
# line 121
    "symbol_type": symbol_type,
# line 122
    "chart_type": chart_type,
# line 123
    "time_interval": time_interval
# line 124
}


# line 127
st.subheader("Generated Payload")

# line 128
st.json(payload)


# line 131
download_button = st.button(
# line 132
    label="Download OHLC Data",
# line 133
    use_container_width=True
# line 134
)


# line 137
if download_button:

    # line 139
    with st.spinner("Fetching NSE market data..."):

        try:

            # line 143
            response = requests.post(
            # line 144
                FASTAPI_URL,
            # line 145
                json=payload,
            # line 146
                timeout=60
            # line 147
            )

            # line 149
            if response.status_code != 200:

                # line 151
                st.error(
                # line 152
                    f"Backend Error: {response.text}"
                # line 153
                )

            else:

                # line 157
                data = response.json()

                # line 159
                df = pd.DataFrame(data)

                # line 161
                st.success(
                # line 162
                    f"Downloaded {len(df)} candles"
                # line 163
                )

                # line 165
                st.subheader("OHLC Data")

                # line 167
                st.dataframe(
                # line 168
                    df,
                # line 169
                    use_container_width=True,
                # line 170
                    height=500
                # line 171
                )

                # line 173
                csv_data = df.to_csv(index=False)

                # line 175
                st.download_button(
                # line 176
                    label="Download CSV",
                # line 177
                    data=csv_data,
                # line 178
                    file_name=f"{trade_name}_ohlc.csv",
                # line 179
                    mime="text/csv"
                # line 180
                )

        except Exception as error:

            # line 184
            st.error(
            # line 185
                f"Application Error: {error}"
            # line 186
            )

# # line 1
# uvicorn app.api.main:app --reload
# ```

# ```bash
# # line 1
# streamlit run frontend/streamlit_app.py
# ```
