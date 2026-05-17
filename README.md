# NSE Data Retrieval API

A lightweight backend API built using FastAPI for downloading and searching historical NSE stock market data.  
This project fetches OHLC candle data directly from NSE charting endpoints and provides clean REST APIs for symbol lookup, search, and historical data retrieval.

---

## Features

- Historical OHLC candle data download
- NSE symbol and token search
- FastAPI-based REST APIs
- Input validation using Pydantic
- Query filtering and sorting
- JSON response support
- Token master generation from Angel One OpenAPI data

---

## Tech Stack

- Python
- FastAPI
- Pandas
- Requests
- Pydantic

---

## Project Structure

```bash
NSE_DATA/
│
├── app/
│   ├── services/
│   │   └── NSE_Charting.py
│   └── main.py
│
├── Data/
│   └── tokens.json
│
├── Equity_token.csv
└── angel_scripmaster_to_csv.py
```

---

## API Endpoints

### GET `/`
Health check endpoint.

### GET `/about`
Returns project information.

### GET `/view`
View all available trading symbols.

### GET `/symbol_name/{traded_symbol}`
Fetch token details for a specific NSE symbol.

Example:
```bash
/symbol_name/ICICIBANK-EQ
```

### GET `/search`
Search symbols using partial keyword matching.

Example:
```bash
/search?symbol_name=bank&order=asc
```

### POST `/download`
Download historical candle data.

Example Request:
```json
{
  "trade_name": "ICICIBANK-EQ",
  "token": 4963,
  "from_date": "2026-05-01T00:00:00",
  "to_date": "2026-05-10T00:00:00",
  "symbol_type": "Equity",
  "chart_type": "D",
  "time_interval": 1
}
```

---

## How It Works

The project:
1. Downloads symbol master data
2. Filters NSE equity instruments
3. Generates token mappings
4. Calls NSE historical chart APIs
5. Converts response into structured OHLC DataFrames

---

## Run Locally

Install dependencies:
```bash
pip install -r requirements.txt
```

Start server:
```bash
uvicorn app.main:app --reload
```

Open Swagger Docs:
```bash
http://127.0.0.1:8000/docs
```

---

## Future Improvements

- WebSocket realtime streaming
- Database integration
- Async request handling
- Backtesting engine
- Strategy deployment support
- Docker deployment

---

## Author

ARPIT  
Aspiring AI Engineer & Backend Developer
