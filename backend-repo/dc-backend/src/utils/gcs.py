from google.cloud import storage
import gspread
import pandas as pd
import os

gcp_credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
gc = gspread.service_account(filename=gcp_credentials)

def get_spreadsheet(spreadsheet_id, sheet_name):
    sheet = gc.open_by_key(spreadsheet_id)
    ws = sheet.worksheet(sheet_name)
    return pd.DataFrame(ws.get_all_records())

class GCSClient():
    def __init__(self, project_id="vertex-355415"): 
        self.storage_client = storage.Client(project_id)
        
    def download_file(self, bucket_name, bucket_object, destination_filename):
        bucket = self.storage_client.get_bucket(bucket_name) 
        blob = bucket.blob(bucket_object) 
        blob.download_to_filename(destination_filename)
        
    def upload_file(self, src_filename, bucket_name, bucket_object):
        bucket = self.storage_client.get_bucket(bucket_name)  
        blob = bucket.blob(bucket_object)
        blob.upload_from_filename(src_filename) 