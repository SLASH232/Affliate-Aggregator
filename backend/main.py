from scrapper.scrape_product_info import Product
from scrapper.scrape_commission_rates import Scrape_commission_rate
from scrapper.scrape_config import stores, commission_rate_link
from bigquery.bigquery_utility import BigqueryUtility
from bigquery.schemas import product_schema
from config import config
import asyncio
from fuzzywuzzy import fuzz
import pandas as pd
import random
import string
import time
from datetime import datetime,timezone

def generate_custom_id(key):
    timestamp = str(int(time.time()))
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{key}{timestamp}{random_chars}"


def get_category_rate(category_table_df,prd_cat):
    best_match_rate=0
    best_match_score=0
    best_match_category=None
    prd_cat=prd_cat.strip().lower()
    for index,row in category_table_df.iterrows():
        categories= row['category'].split('|')
        for category in categories:
            similarity_score= fuzz.token_sort_ratio(prd_cat,category.strip().lower())
            if similarity_score>best_match_score:
                best_match_score=similarity_score
                best_match_category=row['category']
                best_match_rate=row['rate']
    
    return {"category":best_match_category,"rate":best_match_rate}

async def get_load_commission_rates_bq():
    scr=Scrape_commission_rate() 
    store_cdf= await scr.start()
    bq=BigqueryUtility(project_id=config['project_id'],dataset_id=config['dataset_id'],table_id=config['commission_table_id']) 
    for store in stores:
        bq.load_data_to_bq(store_cdf[store])
    return "fetched and loaded to bq successfully!"


def get_commission_rate_bq(category,store):
    bq=BigqueryUtility(project_id=config['project_id'],dataset_id=config['dataset_id'],table_id=config['commission_table_id']) 
    query=f"""
    WITH ranked_products AS (
        SELECT
            *,
            CASE
                WHEN REGEXP_CONTAINS(category, r'(?i){category}') THEN 1
                WHEN REGEXP_CONTAINS(category, r'(?i){category[:4]}') THEN 2
                WHEN LENGTH(category) - LENGTH('{category}') BETWEEN -3 AND 3 THEN 3
                ELSE 4
            END AS rank
        FROM `data-terminus-423716-d6.affiliate.commission_rates`
        WHERE store = '{store}'
    )
    SELECT *
    FROM ranked_products
    ORDER BY rank, LENGTH(category) - LENGTH('{category}') ASC
    LIMIT 1
    """
    df=bq.read_data_from_bq(query)
    return {'rate':df['rate'].iloc[0],'category':df['category'].iloc[0],'cid':df['cid'].iloc[0]}
    
async def compared_commission_rates(product_link):
    p=Product()
    product_response= await p.get_product_info(product_link=product_link,store="amazon")
    category=product_response['category']
    res={}
    
    for store in stores:
     rate=get_commission_rate_bq(category,store)['rate']
     res[store]=rate
    return res

def get_result_bq():
    bq=BigqueryUtility(project_id=config['project_id'],dataset_id=config['dataset_id'],table_id=config['product_table_id']) 
    query=f""" 
        SELECT pid,title,
        CASE when count(in_stock)=0 THEN 'In-Active' 
            ELSE 'Active'
            END AS status
          from `data-terminus-423716-d6.affiliate.products_info`
          Group by pid ,title
"""
    df=bq.read_data_from_bq(query)
    return df
def get_url(pid):
    bq=BigqueryUtility(project_id=config['project_id'],dataset_id=config['dataset_id'],table_id=config['product_table_id']) 
  
    query=f"""
        SELECT url FROM `data-terminus-423716-d6.affiliate.products_info`
        WHERE pid='{pid}' and in_stock=True
        ORDER BY commission_rate             
        limit 1       
"""
    df=bq.read_data_from_bq(query)
    url=df['url'].iloc[0]
    return url

async def start(urls, title, keyword, response_route):
    pid=generate_custom_id('p')
    product_list=[]
    for store in stores:  
        # get the product info first
        p=Product()
        product_response= await p.get_product_info(product_link=urls[store],store=store)
        
        # commission rate
        product_response['pid']=pid
        product_response['title']=title
        product_response['store']=store
        product_response['url']=urls[store]
        crc=get_commission_rate_bq(product_response['category'],store)
        product_response['commission_rate']=crc['rate'] 
        product_response['cid']=crc['cid']
        product_response['last_modified']=datetime.now().replace(second=0,microsecond=0,tzinfo=timezone.utc)
        
        product_list.append(product_response)
    
    print("Saving results.")
    bq=BigqueryUtility(project_id=config['project_id'],dataset_id=config['dataset_id'],table_id=config['product_table_id']) 
    bq.create_dataset_if_not_exists(product_schema)
    bq.load_data_to_bq(pd.DataFrame(product_list))
    return "DONE!"
        



if __name__ == "__main__":
    # test script
    p =Product()
    print(asyncio.run(get_url('p1716303030SPIK')))
        # start({'amazon':'https://amzn.to/4dIsQPD','flipkart':'https://www.flipkart.com/muscleblaze-bullet-shaker-leakproof-gym-bottle-supplements-500-ml/p/itmf3e0c8d8829b4?pid=BOTGVQ9SZWMTRZUH&lid=LSTBOTGVQ9SZWMTRZUHT6Z86K&marketplace=FLIPKART&cmpid=content_bottle_8965229628_gmc'},'MuscleBlazeBottle',"","")))
        # p.get_product_info(product_link="https://amzn.to/3CkMzmI",store="amazon")))
        # get_load_commission_rates_bq()))
        # compared_commission_rates("https://amzn.to/3CkMzmI")))
