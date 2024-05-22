# from main import main
import sys
import asyncio
# from config import amazon_product_config
from main import start
if __name__ == '__main__':
    # Extract command-line arguments
    if len(sys.argv) < 5:
        print('Usage: python -m package_name url search_text endpoint')
        sys.exit(1)

    urls={
        "amazon":sys.argv[1],
        "flipkart": sys.argv[2]
        }
    title = sys.argv[3]
    keyword = sys.argv[4]
    endpoint = sys.argv[5]


    # Run the scraper asynchronously
    asyncio.run(start(urls,title,keyword, endpoint))
