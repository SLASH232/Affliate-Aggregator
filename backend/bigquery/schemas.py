from google.cloud import bigquery

commission_schema=[
    bigquery.SchemaField("category","STRING"),
    bigquery.SchemaField("rates","FLOAT"),
    bigquery.SchemaField("store","STRING"),
    bigquery.SchemaField("last_modified","TIMESTAMP"),
    bigquery.SchemaField("cid","STRING")
]
product_schema=[
    bigquery.SchemaField("pid","STRING"),
    bigquery.SchemaField("title","STRING"),
    bigquery.SchemaField("name","STRING"),
    bigquery.SchemaField("url","STRING"),
    bigquery.SchemaField("price","STRING"),
    bigquery.SchemaField("category","STRING"),
    bigquery.SchemaField("store","STRING"),
    bigquery.SchemaField("in_stock","BOOLEAN"),
    bigquery.SchemaField("cid","STRING"),
    bigquery.SchemaField("commission_rate","FLOAT"),
    bigquery.SchemaField("last_modified","TIMESTAMP"),
    
]