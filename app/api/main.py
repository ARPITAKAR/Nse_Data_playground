from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field,field_validator
from typing import Literal, Annotated, Optional
import json
import re
from datetime import datetime
from app.services.NSE_Charting import get_ohlc

app = FastAPI()
'''
The Path() function in FastAPI is used to add validation,
metadata, and documentation for path parameters.

Common options:
- title        : Short name for parameter
- description  : Detailed explanation
- example      : Sample value
- ge           : Greater than or equal
- gt           : Greater than
- le           : Less than or equal
- lt           : Less than
- min_length   : Minimum string length
- max_length   : Maximum string length
- regex        : Pattern validation
'''
'''
HTTPException is a built-in exception in FastAPI
used to return custom HTTP error responses.

It helps handle errors gracefully instead of
crashing the server.

Features:
- Return proper status codes (404, 400, 403, etc.)
- Send custom error messages
- Add optional headers
'''

def load_data():
    with open('C:/Users/Arpit/Desktop/NSE_DATA/Data/tokens.json','r') as f:
        data=json.load(f)
    
    return data 

class UserInput(BaseModel):
    trade_name: Annotated[str, Field(...,description='Symbol to be data downloaded')]
    token: Annotated[Optional[int], Field(default=None)]
    from_date : Optional[datetime] = None
    to_date : Annotated[datetime,Field(...,description='Pydantic validates ISO 8601 strings (e.g., "2026-05-10")')]                      
    symbol_type: Literal["Equity","Futures","Options"]
    chart_type : Annotated[Literal["I","D","W","M"],Field(...,description='Intraday,Daily,Weekly')]
    time_interval : Annotated[Literal[1,5,15,30,60],Field(description='timeinterval of candles')]
    
    
    @field_validator('trade_name')
    @classmethod
    def symbol_case(cls,value):
        return value.upper()
        

@app.post('/download')
def stock_data(data: UserInput):

    try:

        from_unix = (
            int(data.from_date.timestamp())
            if data.from_date
            else 0
        )

        to_unix = int(
            data.to_date.timestamp()
        )

        df = get_ohlc(
            token=data.token,
            symbol=data.trade_name,
            from_date=from_unix,
            to_date=to_unix,
            time_interval=data.time_interval,
            chart_type=data.chart_type,
            symbol_type=data.symbol_type
        )

        return df.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )




@app.get("/")
def hello():
    return {'Message':'Stock Data retrival System API'}

@app.get('/about')
def about():
    return {'message': 'NSE Data Downloader System'}

@app.get('/view')
def view():
    data = load_data()
    
    return data
'''
Query() is a utility function in FastAPI used to
declare, validate, and document query parameters.

Uses:
- Set default values
- Apply validation rules
- Add metadata for API documentation

Common Parameters:
- default       : Set default value
- title         : Display name in docs
- description   : Detailed explanation
- example       : Sample input value
- examples      : Multiple sample inputs
- min_length    : Minimum string length
- max_length    : Maximum string length
- ge            : Greater than or equal
- gt            : Greater than
- le            : Less than or equal
- lt            : Less than
- regex         : String pattern validation
'''
@app.get('/symbol_name/{traded_symbol}')
def view_symbol(traded_symbol: str= Path(...,description = 'Traded symbol name',examples='TATATECH-EQ')):
    # load all the trade_name token numbers
    data = load_data()
    
    if traded_symbol in data:
        return data[traded_symbol]
    raise HTTPException(status_code=404,detail='Symbol not found')

@app.get('/search')
def search_sort(symbol_name: str = Query(...,description='Search similar traded names'), order: str= Query('asc',description='sort in asc or desc order as per token number')):
    
    
    data = load_data()
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail= "order must be asc or desc")
                            
    pattern = re.compile(
        re.escape(symbol_name),re.IGNORECASE
    )
    
    matched_data = []
    
    for key,value in data.items():
        symbol = value.get("symbol", "")
        name = value.get("name", "")
        
        if (pattern.search(symbol) or pattern.search(name)):
            matched_data.append(value)
    sort_order = True if order=='desc' else False
    
    matched_data.sort(key=lambda x:int(x["token"]),reverse=sort_order)
    
    return {'Total_match': len(matched_data),
        "results": matched_data
    }