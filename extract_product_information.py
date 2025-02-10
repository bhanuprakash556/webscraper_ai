import asyncio
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup

async def extract_product_info(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url)
        if result.success:
            # Use 'lxml' for faster parsing
            soup = BeautifulSoup(result.html, 'lxml')  

            product_info = {}

            # Extract product title
            title_tag = soup.select_one('div.product-specification > h1.sc-39506017-0.eaptXk.product-title')
            product_info['product_title'] = title_tag.get_text(strip=True) if title_tag else 'N/A'

            # Extract price
            price_tag = soup.select_one('div.price-section')
            product_info['price'] = price_tag.get_text(strip=True) if price_tag else 'N/A'

            # Extract product specifications from table
            specs_table = soup.select_one('table.spec-table')
            if specs_table:
                specs = {row.select_one('td:nth-of-type(1)').get_text(strip=True): 
                         row.select_one('td:nth-of-type(2)').get_text(strip=True) 
                         for row in specs_table.find_all('tr') if len(row.find_all('td')) == 2}
                product_info['product_specifications'] = specs
            else:
                product_info['product_specifications'] = 'N/A'

            # Extract other details using optimized CSS selectors
            product_info['product_overview'] = soup.select_one('div.sc-39506017-0.xHZay.overflow-x.seo-content')
            product_info['product_overview'] = product_info['product_overview'].get_text("\n", strip=True) if product_info['product_overview'] else 'N/A'

            product_info['company_details'] = soup.select_one('div.sc-39506017-0.xHYXW.overflow-x.seo-content')
            product_info['company_details'] = product_info['company_details'].get_text("\n", strip=True) if product_info['company_details'] else 'N/A'

            # product_info['company_details'] = soup.select_one('div.sc-39506017-0.xHYXW.overflow-x.seo-content')
            # product_info['company_details'] = product_info['company_details'].get_text("\n", strip=True) if product_info['company_details'] else 'N/A'

            product_info['business_details'] = soup.select_one('div.business-details')
            product_info['business_details'] = product_info['business_details'].get_text("\n", strip=True) if product_info['business_details'] else 'N/A'

            product_info['seller_details'] = soup.select_one('div.sc-2d50e193-0.kIqqhV')
            product_info['seller_details'] = product_info['seller_details'].get_text("\n", strip=True) if product_info['seller_details'] else 'N/A'

            # Extract vendor name
            vendor_name_tag = soup.select_one('div.seller-logo-name-cont > a.seller-name-url > h2.sc-39506017-0.gogMcY')
            product_info['vendor_name'] = vendor_name_tag.get_text(strip=True) if vendor_name_tag else 'N/A'

            # Store product URL
            product_info['product_url'] = url

            return product_info
        else:
            print(f"Failed to retrieve the page: {result.error_message}")
            return None

if __name__ == "__main__":
    product_url = "https://www.tradeindia.com/products/examination-gloves-non-sterile-pre-powdered-565239.html"
    product_details = asyncio.run(extract_product_info(product_url))
    if product_details:
        print("\nExtracted Product Information:")
        for key, value in product_details.items(): 
            print(f"{key}: {value}")
