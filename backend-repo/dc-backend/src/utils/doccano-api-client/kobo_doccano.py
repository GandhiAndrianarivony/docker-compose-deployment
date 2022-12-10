import os
import json

import requests
from doccano_client import DoccanoClient
from ingest_to_db import DCAnalytics
from connect_to_db import MongoDB

from dotenv import load_dotenv

import click
from tqdm import tqdm


# PARAMETERS
load_dotenv()

KOBO_PASSWORD = os.environ['KOBO_PASSWORD']
KOBO_USERNAME = os.environ['KOBO_USERNAME']

DOCCANO_USERNAME = os.environ['DOCCANO_USERNAME']
DOCCANO_PASSWORD = os.environ['DOCCANO_PASSWORD']


class Kobo2Doccano:
    """
    DESCRIPTION:
    PARAMETERS:
        doccano_project_id:
        doccano_format:
            - AudioFile
    """

    def __init__(
        self,
        doccano_project_id=3,
        doccano_format='AudioFile',
        doccano_column_data='text',
        doccano_column_label='label'
    ):
        self.doccano_project_id = doccano_project_id
        # self.doccano_task = doccano_task_type
        self.doccano_format = doccano_format
        self.doccano_column_data = doccano_column_data
        self.doccano_column_label = doccano_column_label

        # Login to Doccano
        self.doccano = DoccanoClient('https://doccano.haizaha.com', True)
        self.doccano.login(DOCCANO_USERNAME, DOCCANO_PASSWORD)

        # Instance of mongo
        self.mongo = MongoDB()

        # Kobo session
        self.session = requests.Session()
        self.session.auth = (KOBO_USERNAME, KOBO_PASSWORD)

    def upload_audio_from_doccano(
        self,
        kobo_form_id,
        kobo_audio_quality,
        doccano_task_type
    ):
        self.mongo.connect()
        file_paths = self.mongo.fetch_audio_data(
            kobo_form_id, kobo_audio_quality)
        temp_dir = "temp_directory"
        os.makedirs(temp_dir, exist_ok=True)

        for file in tqdm(file_paths):
            response = self.session.get(file['url'])
            iter = 0
            while response.status_code != 200:
                response = self.session.get(file['url'])
                print(f'Status Code {response.status_code}')
                iter += 1
                if iter == 5:
                    print('Failed to download file.')
                    break

            if iter != 5:
                with open(f"{temp_dir}/{file['filename']}_instanceID_{file['_id']}.mp3", 'wb') as flaudio:
                    flaudio.write(response.content)

            self.doccano.upload(
                project_id=self.doccano_project_id,
                file_paths=[
                    f"{temp_dir}/{file['filename']}_instanceID_{file['_id']}.mp3"],
                task=doccano_task_type,
                format=self.doccano_format,
                column_data=self.doccano_column_data,
                column_label=self.doccano_column_label,
            )
            os.remove(
                f"{temp_dir}/{file['filename']}_instanceID_{file['_id']}.mp3")

    def download_data_from_doccano(self, doccano_project_id, doccano_down_format, only_approved, dir_name):
        print(f"Download in progress ...")
        filepath = self.doccano.download(
            doccano_project_id,
            doccano_down_format,
            only_approved,
            dir_name
        )
        return filepath
