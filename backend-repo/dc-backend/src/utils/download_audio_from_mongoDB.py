# The version of pymongo which is compatible with mongoDB==3.4 is pymongo==3.12.3
# pip3 install pymongo==3.12.3
import pymongo

import requests
from requests.auth import HTTPBasicAuth
import click
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

# PARAMETERS
MONGODB_NAME = os.environ['MONGODB_NAME']
MONGODB_USER = os.environ['MONGODB_USER']
MONGODB_PASSWORD = os.environ['MONGODB_PASSWORD']
MONGODB_COLLECTION_NAME = os.environ['MONGODB_COLLECTION_NAME']
URL = os.environ['URL']
KOBO_PASSWORD = os.environ['KOBO_PASSWORD']
KOBO_USERNAME = os.environ['KOBO_USERNAME']

def conn2mongo():
    client = pymongo.MongoClient(
        f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{URL}/")
    db = client[MONGODB_NAME]
    client.close()
    return db


def download_audio(url, fdest, fn):
    sc = 401
    iter = 0
    while sc != 200:
        res = requests.get(url, auth=HTTPBasicAuth(
            KOBO_USERNAME, KOBO_PASSWORD))
        sc = res.status_code
        print(f'status code {sc}')
        iter += 1
        if iter == 5:
            break
        sleep(10)

    with open(f'{fdest}/{fn}.mp3', 'wb') as flaudio:
        flaudio.write(res.content)
    print(f'Success downloading - filename: {fn} !!!')


@click.command()
@click.option(
    '--form-id',
    type=click.STRING,
    required=True
)
@click.option(
    '--audio-quality',
    default='download_url',
    type=click.Choice([
        "download_url",
        "download_small_url",
        "download_medium_url",
        "download_large_url"
    ])
)

def kobo_audio_download(form_id, audio_quality):
    db = conn2mongo()

    fetchedData = list(db[MONGODB_COLLECTION_NAME].find({'_xform_id_string': form_id}))
    os.makedirs('back-up', exist_ok=True)
    click.echo(f"Audio Quality {audio_quality}")
    for fd in fetchedData:
        for att in fd['_attachments']:
            download_audio(att[audio_quality], './back-up',
                           os.path.basename(att['filename']).split('.')[0])


if __name__ == '__main__':
    kobo_audio_download()

