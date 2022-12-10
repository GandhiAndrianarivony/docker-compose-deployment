import json
import os


def mapping(df, cmap_file):
    dataframe = df.copy()
    cmap_mongo2postgres = json.load(
        open(os.path.join("data", cmap_file)))

    used_cols = [i['mongo_key'] for i in cmap_mongo2postgres]
    dataframe = dataframe[used_cols]

    for k in cmap_mongo2postgres:
        dataframe.rename(
            columns={k['mongo_key']: k['postgres_key']}, inplace=True)

    dataframe.fillna('', inplace=True)
    return dataframe
