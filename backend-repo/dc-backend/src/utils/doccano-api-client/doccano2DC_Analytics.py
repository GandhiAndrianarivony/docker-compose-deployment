import click
from kobo_doccano import Kobo2Doccano
from ingest_to_db import DCAnalytics

import pandas as pd
import json
import os


@click.command()
@click.option(
    '--doccano-project-id',
    required=True
)
@click.option(
    '--doccano-format', required=True,
    type=click.Choice([
        "JSONL"  # used when downloading is performed
    ])
)
def main(
    doccano_project_id,
    doccano_format,  # Export format JSONL
):
    k2d = Kobo2Doccano(
        doccano_project_id=doccano_project_id,
        doccano_format=doccano_format,
    )
    profile = k2d.doccano.get_profile()
    username = profile.username

    dir_name = f"./annotation_download/project_id_{doccano_project_id}"
    filepath = k2d.download_data_from_doccano(doccano_project_id,
                                                doccano_format,
                                                only_approved=True,
                                                dir_name=dir_name)

    # extract filepath zip inside dir_name
    os.makedirs(dir_name, exist_ok=True)
    import zipfile
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(dir_name)

    # Load data
    with open(os.path.join(dir_name, f"{str(username)}.jsonl")) as dt:
        dt = dt.read().split('\n')[:-1]
        data = []
        for d in dt:
            data.append(json.loads(d))

    output = []
    for d in data:
        mongo_instance_id = d["filename"].split('_')[-1].split('.')[0]
        output.append(
            {
                'annotation_id': d['id'],
                'mongo_instance_id': mongo_instance_id,
                'audio_filename': d['filename'],
                'label': d['label'],
                'comment': d['Comments']
            }
        )
    # print(output)
    dataframe = pd.DataFrame(output)
    print(dataframe.dtypes)
    os.remove(filepath)
    os.remove(os.path.join(dir_name, f"{str(username)}.jsonl"))
    # # Convert the array of dicts into dataframe
    hzh_dc_analytics = DCAnalytics()
    hzh_dc_analytics.ingest(dataframe, table_name="doccano_speech2text")


if __name__ == "__main__":
    main()

# Example:
# -------
# python3 doccano2DC_Analytics.py --doccano-project-id=3 --doccano-format=JSONL
