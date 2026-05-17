import psycopg2
from psycopg2.extras import RealDictCursor
from Credentials.credentials import Cred


curr,conn= None,None
# token	symbol name expiry strike lotsize instrumenttype exch_seg tick_size
# get_ohlc(
#     token: int,
#     symbol: str,
#     from_date: int,
#     to_date: int,
#     time_interval: int = 5,
#     chart_type: str="I",
#     symbol_type: str = "Equity"
# ) -> pd.DataFrame:
# df = df[["Datetime","Open","High","Low","Close","Volume"]]
try:
    
    with psycopg2.connect(
        host= Cred.hostname,
        dbname = Cred.database,
        user = Cred.username,
        port = Cred.port_id,
        password = Cred.pwd 
    ) as conn:
        with conn.cursor(cursor_factory= RealDictCursor) as curr:
            curr.execute('DROP TABLE IF EXISTS symbols')
            create_table1 = '''
            CREATE TABLE symbols (
            token BIGINT PRIMARY KEY,
            symbol VARCHAR(30),
            name VARCHAR(100),
            exchange VARCHAR(10),
            instrument_type VARCHAR(20)
            );
            '''
            curr.execute(create_table1)
            conn.commit()
            
            
            curr.execute('DROP TABLE IF EXISTS historical_data')
            create_table2 = '''
            CREATE TABLE historical_data (
            id BIGSERIAL PRIMARY KEY,
            token BIGINT,
            symbol VARCHAR(30),
            timeframe VARCHAR(10),
            datetime TIMESTAMP,
            open NUMERIC(12,2),
            high NUMERIC(12,2),
            low NUMERIC(12,2),
            close NUMERIC(12,2),
            volume BIGINT,
            UNIQUE(token, timeframe, datetime)
            );
            '''
            curr.execute(create_table2)
            conn.commit()
            
except Exception as e:
    print(f'Problem in Database{e}')