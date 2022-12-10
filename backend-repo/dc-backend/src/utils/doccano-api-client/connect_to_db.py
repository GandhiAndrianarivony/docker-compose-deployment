
from typing import List
import pymongo
from sqlalchemy import create_engine
from sqlalchemy.engine import URL as url

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
        self.db=None

    def connect(self):
        client = pymongo.MongoClient(
            f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{URL}:{MONGODB_PORT}/")
        self.db = client[MONGODB_NAME]
        client.close()

    def fetch_audio_data(self, form_id, audio_quality) -> List[str]:
        data = list(self.db[MONGODB_COLLECTION_NAME].find(
            {'_xform_id_string': form_id}))
        audio_url_lists = []
        for fd in data:
            _id = fd['_id']
            for att in fd['_attachments']:
                audio_url_lists.append({'url': att[audio_quality], 'filename': os.path.basename(
                    att['filename']).split('.')[0], '_id': _id})
        return audio_url_lists



class PostgresDB:
    def __init__(self):
        self.engine=None

    def connect(self):
        url_object = url.create(
            "postgresql+psycopg2",
            username=POSTEGRESDB_USER,
            password=POSTEGRESDB_PASSWORD,
            host=URL,
            port=POSTEGRESDB_PORT,
            database=POSTEGRESDB_NAME
        )
        self.engine = create_engine(url_object)
            # f"postgresql+psycopg2://{POSTEGRESDB_USER}:{POSTEGRESDB_PASSWORD}\@{URL}:{POSTEGRESDB_PORT}/{POSTEGRESDB_NAME}")

    def ingest(self, dataframe, table_name):
        dataframe.to_sql(table_name, self.engine, if_exists='replace')