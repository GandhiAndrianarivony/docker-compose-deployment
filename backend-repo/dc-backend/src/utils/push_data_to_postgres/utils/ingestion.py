from utils.db import PostgresDB

def ingest(df, table_name, dest, ngo):
    postgres = PostgresDB()
    try:
        postgres.backup(table_name=table_name, dest=dest, ngo=ngo)
    except:
        pass
    postgres.ingest(df, table_name)
