from playwright.async_api import async_playwright
from .scrape_config import product_config
import pandas as pd


class Product:

    def cleanString(self,incomingString):
        newstring = incomingString
        newstring = newstring.replace("!","")
        newstring = newstring.replace("@","")
        newstring = newstring.replace("#","")
        newstring = newstring.replace("$","")
        newstring = newstring.replace("%","")
        newstring = newstring.replace("^","")
        newstring = newstring.replace("&","and")
        newstring = newstring.replace("*","")
        newstring = newstring.replace("(","")
        newstring = newstring.replace(")","")
        newstring = newstring.replace("+","")
        newstring = newstring.replace("=","")
        newstring = newstring.replace("?","")
        newstring = newstring.replace("\'","")
        newstring = newstring.replace("\"","")
        newstring = newstring.replace("{","")
        newstring = newstring.replace("}","")
        newstring = newstring.replace("[","")
        newstring = newstring.replace("]","")
        newstring = newstring.replace("<","")
        newstring = newstring.replace(">","")
        newstring = newstring.replace("~","")
        newstring = newstring.replace("`","")
        newstring = newstring.replace(":","")
        newstring = newstring.replace(";","")
        newstring = newstring.replace("|","")
        newstring = newstring.replace("\\","")
        newstring = newstring.replace("/","")    
        newstring=newstring.replace("›","")    
        newstring=newstring.replace("\n"," ")   
        newstring=newstring.replace(".","")    
        return newstring

    async def scrape(self,page,prd_config):

        product_page= await page.query_selector(f"[{prd_config["main"]["attr"]} = {prd_config["main"]["value"]}]")
        title_content=await product_page.query_selector(f"{prd_config["product_title"]["value"]}")
        price_content=await product_page.query_selector(f"{prd_config["product_price"]["value"]}")
        instock_content=await product_page.query_selector(f"{prd_config["product_instock"]["value"]}")
        
        title= await title_content.inner_text()
        price= await price_content.inner_text()
        instock=False
        if(instock_content):
            instock=True
        


        print(f"{title}, {price}, {instock}")
       
        category_content= await page.query_selector(f"{prd_config["product_category"]["value"]}")
        price=self.cleanString(price)
        category= self.cleanString( await category_content.inner_text())
        print(category)
        return {'name':title.strip(),'price':price.strip(),'in_stock':instock,'category':category.strip()}


    async def get_product_info(self,product_link,store):

        async with async_playwright() as pw:
            print("Connecting to browser.")
            browser = await pw.chromium.launch()
            page = await browser.new_page() 

            await page.goto(product_link)
            product_response=await self.scrape(page,product_config[store])
         
                
            await browser.close()

        return product_response