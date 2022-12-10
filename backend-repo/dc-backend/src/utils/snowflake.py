from snowflake.connector.pandas_tools import pd_writer
import pandas as pd
from sqlalchemy import create_engine 
import json
from snowflake.sqlalchemy import URL

credentials = json.load(open("/Users/mendrika/.snowflake/credentials.json"))

user = credentials["SNOWFLAKE_USERNAME"]
password = credentials["SNOWFLAKE_PASSWORD"]
account = "tw81295.us-central1.gcp"

def get_engine(db, schema, warehouse):   
    connection_string = URL( 
        user=user,
        password=password,
        account=account,
        database=db,
        schema=schema,
        warehouse=warehouse
    )
    engine = create_engine(connection_string)
    return engine

def update_table(engine, table_name, df, if_exists="replace"): 
    with engine.connect() as con:
        df.columns = map(lambda x: str(x).upper(), df.columns)
        df.to_sql(name=table_name.lower(), con=con, if_exists=if_exists, index=False, index_label=None)
