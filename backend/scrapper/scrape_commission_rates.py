from playwright.async_api import async_playwright
from .scrape_config import stores,commission_config,commission_rate_link
import pandas as pd
import random
import string
import time
from datetime import datetime,timezone
import re
class Scrape_commission_rate:
    def extract_float_from_string(self,s):
        pattern = r"[-+]?\d*\.\d+|\d+"
        match = re.search(pattern, s)
        if match:
            return float(match.group())
        else:
            return None
        
    def generate_custom_id(self,key):
        timestamp = str(int(time.time()))
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"{key}{timestamp}{random_chars}"
    
    async def scrape(self,page,com_config):
        table_content=await page.wait_for_selector(com_config["value"])
        
        rows_content= await table_content.query_selector_all('tbody tr')
        cat_rate_ls=[]
        for row in rows_content:
            tr={}
            cell= await row.query_selector_all('td')
            if(cell):
                tr['category']= await cell[0].inner_text()
                tr['rate']=self.extract_float_from_string(await cell[1].inner_text())
                cat_rate_ls.append(tr)
                tr['cid']=self.generate_custom_id("c")
                tr['last_modified']=datetime.now().replace(second=0,microsecond=0,tzinfo=timezone.utc)
        
        df=pd.DataFrame(cat_rate_ls)
        return df
    
    async def start(self):
        store_commission_rate_df={}
        async with async_playwright() as pw:
            print("Connecting to browser.")
            browser = await pw.chromium.launch()
            page = await browser.new_page() 

            for store in stores:  
                # commission rate
                await page.goto(commission_rate_link[store], timeout=120000)
                
                rate_df= await self.scrape(page,commission_config[store])
                rate_df['store']=store
                store_commission_rate_df[store]=rate_df
                
            await browser.close()

        return store_commission_rate_df