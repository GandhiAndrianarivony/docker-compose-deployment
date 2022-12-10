from connect_to_db import PostgresDB

class DCAnalytics:
    def __init__(self):
        self.postgresdb = PostgresDB()

    def ingest(self, dataframe, table_name):
        self.postgresdb.connect()
        self.postgresdb.ingest(dataframe, table_name)
