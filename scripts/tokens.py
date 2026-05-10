# filename: angel_scripmaster_to_csv.py

# line 1
import requests
import json
# line 2
import pandas as pd

# line 4
URL = (
# line 5
    "https://margincalculator.angelbroking.com/"
# line 6
    "OpenAPI_File/files/OpenAPIScripMaster.json"
# line 7
)

# line 9
response = requests.get(URL)

# line 11
data = response.json()

converted_data = {}

# Line 4
for item in data:
    symbol = item["symbol"]
    converted_data[symbol] = item

# Line 5
with open("tokens.json", "w") as f:
    json.dump(converted_data, f, indent=4)

# line 13
df = pd.DataFrame(data)

# file: filter_dataframe.py

# Line 1
filtered_df = df[
# Line 2
    (df["instrumenttype"] == "") &
# Line 3
    (df["exch_seg"] == "NSE")
# Line 4
]


# line 15
print(filtered_df.tail())

# line 17
print(filtered_df.columns)

# line 19
df.to_csv(
# line 20
    "Equity_token.csv",
# line 21
    index=False
# line 22
)

# line 24
print(
# line 25
    "CSV saved as Equity_token.csv"
# line 26
)