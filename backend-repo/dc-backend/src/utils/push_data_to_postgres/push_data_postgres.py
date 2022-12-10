from utils.db import MongoDB
from utils.generate_json_mapping_cols import get_key_mapping
from utils.pnud_tfsm import column_tfsm
from utils.ingestion import ingest
import pandas as pd
import click
from utils.mongo_postgres_mapping import mapping
import re

# ngo='pnud',
# form_id="a3sZ4KTCLhspWRxgoUCTFK",
# cmap_file='eisa_cmap.json',
# tab_name='fisy_fanadihadina'


@click.command()
@click.option(
    '--ngo',
    default='pnud',
    type=click.Choice([
        'pnud',
        'usaid'
    ]),
    required=True
)
@click.option(
    '--form-id',
    required=True
)
@click.option(
    '--cmap-file',
    required=True,
    type=click.STRING,
    help="Name of the the file which contain mapping between mongo key to postgres col"
)
@click.option(
    '--tab-name',
    required=True,
    help="The name of the table in postgreSQL db that we want to store collected data from field. Table will be created if not exist"
)
def push_data(
    ngo,
    form_id,
    cmap_file,
    tab_name
):
    if not re.search(f'\.json$', cmap_file):
        click.echo(
            "😛 The value of the - -cmap-file parameter should contains the .json extension.")
        return

    else:
        mongo = MongoDB()
        fetched_data = mongo.fetch_data(form_id)
        print('\n')
        isMappingFileExist = get_key_mapping(fetched_data, cmap_file)

        if not isMappingFileExist:
            click.echo(
                f"Please, edit the file 'data/{cmap_file}' that should contains your Mongo key to Postgres cols mapping. "
            )

        checking = input(
            f"👌 If you have manually editing the mapping file 'data/{cmap_file}', then type 'yes': ")

        if checking.lower().replace(' ', '') == 'yes':
            df = pd.DataFrame(fetched_data)

            # Mongo -> Postgres mapping
            df = mapping(df, cmap_file)

            if ngo == 'pnud':
                df = column_tfsm(df)

            # Ingest data to PostgreSQL Table
            ingest(df, tab_name, dest='./db-back-up', ngo=ngo)


if __name__ == "__main__":
    push_data()
