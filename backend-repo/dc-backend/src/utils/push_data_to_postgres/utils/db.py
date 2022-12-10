
from typing import List
import pymongo
from sqlalchemy import create_engine
from sqlalchemy.engine import URL as url
import pandas as pd
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_NAME = os.environ['MONGODB_NAME']
MONGODB_USER = os.environ['MONGODB_USER']
MONGODB_PASSWORD = os.environ['MONGODB_PASSWORD']
MONGODB_COLLECTION_NAME = os.environ['MONGODB_COLLECTION_NAME']
MONGODB_PORT = os.environ['MONGODB_PORT']
URL = os.environ['URL']

POSTEGRESDB_NAME = os.environ['POSTEGRESDB_NAME']
POSTEGRESDB_USER = os.environ['POSTEGRESDB_USER']
POSTEGRESDB_PASSWORD = os.environ['POSTEGRESDB_PASSWORD']
POSTEGRESDB_PORT = os.environ['POSTEGRESDB_PORT']


class MongoDB:
    def __init__(self):
        client = pymongo.MongoClient(
            f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{URL}:{MONGODB_PORT}/")
        self.db = client[MONGODB_NAME]
        client.close()

    def fetch_data(self, form_id) -> List[dict]:
        data = list(self.db[MONGODB_COLLECTION_NAME].find(
            {'_xform_id_string': form_id}))
        return data


class PostgresDB:
    def __init__(self):
        url_object = url.create(
            "postgresql+psycopg2",
            username=POSTEGRESDB_USER,
            password=POSTEGRESDB_PASSWORD,
            host=URL,
            port=POSTEGRESDB_PORT,
            database=POSTEGRESDB_NAME
        )
        self.engine = create_engine(url_object)

    def ingest(self, dataframe, table_name):
        dataframe.to_sql(table_name, self.engine, if_exists='replace')

    def backup(self, table_name, dest, ngo):
        os.makedirs(dest, exist_ok=True)
        df = pd.read_sql_table(table_name, self.engine)
        now = datetime.now()
        df.to_csv(
            os.path.join(dest, f"{ngo}-{str(datetime.timestamp(now))}.csv"),
            index=False
        )
        # print(table_name, dest)
