# creating dataset
# updating
# read

from google.cloud import bigquery
from pandas_gbq import gbq
# Construct a BigQuery client object.


class BigqueryUtility:
    def __init__(self,project_id,dataset_id,table_id):
        self.project_id=project_id
        self.dataset_id=dataset_id
        self.table_id=table_id
        self.client = bigquery.Client(project=project_id)
    def create_dataset_if_not_exists(self,schema):
    # Check if the dataset already exist
        table_ref=self.client.dataset(self.dataset_id).table(self.table_id)  # API request
            
        try:
            self.client.get_table(table_ref)
            print(f"table {self.table_id} already exists.")
        except Exception as e:
            # If the dataset does not exist, create it
            print(f"table {self.table_id} does not exist, creating dataset.")
            
            table=bigquery.Table(table_ref=table_ref,schema=schema)
            
            dataset = self.client.create_table(table)  # API request
            print(f"Created table {dataset.project}.{dataset.dataset_id}.{dataset.table_id}")
    
    def load_data_to_bq(self,df):
        gbq.to_gbq(df,
                   destination_table=f"{self.dataset_id}.{self.table_id}",
                   project_id=self.client.project,
                   if_exists='append')
    

    def read_data_from_bq(self,query):
        query_job = self.client.query(query)
        df = query_job.to_dataframe()
        return df
    
    def update_data(self,query):
        query_job = self.client.query(query)
        query_job.result()
        return f"updated {self.dataset_id}  {self.table_id}"