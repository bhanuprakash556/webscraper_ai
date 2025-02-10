import asyncio
import os
import pandas as pd
import re
import time
import subprocess
from crawl4ai import AsyncWebCrawler
from crawl_inside import fetch_tradeindia_links
from extract_product_information import extract_product_info

# Increase file descriptor limit
subprocess.Popen("ulimit -n 100000", shell=True, close_fds=True)

CONCURRENCY_LIMIT = 7

async def limited_arun(crawler, url, semaphore):
    """Limits the number of concurrent web scraping requests."""
    async with semaphore:
        return await crawler.arun(url)

async def get_google_search_links(product: str, location: str, num_pages: int = 5):
    """Scrapes Google search results and filters only TradeIndia vendor links."""
    base_google_url = "https://www.google.com/search?q=site:tradeindia.com+{}+{}&start={}"
    base_tradeindia_url = f"https://www.tradeindia.com/{location.lower()}/"
    formatted_product = "+".join(product.split())
    formatted_location = "+".join(location.split())
    search_links = []
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    
    async with AsyncWebCrawler() as crawler:
        tasks = [
            limited_arun(crawler, base_google_url.format(formatted_product, formatted_location, page * 10), semaphore)
            for page in range(num_pages)
        ]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            if result.success:
                search_results = result.links.get("external", [])
                search_links.extend(
                    link["href"] for link in search_results
                    if "href" in link and link["href"].startswith(base_tradeindia_url)
                )
            else:
                print(f"❌ Failed to scrape Google Search results: {result.error_message}")
    
    return search_links

async def limited_fetch(url, tradeindia_base_url, semaphore):
    """Limits requests to fetch internal product links."""
    async with semaphore:
        return await fetch_tradeindia_links(url, tradeindia_base_url)

async def scrape_inside_urls(inside_urls: list, tradeindia_base_url: str):
    """Scrapes internal product links from multiple TradeIndia vendor pages in parallel."""
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    tasks = [limited_fetch(url, tradeindia_base_url, semaphore) for url in inside_urls]
    results = await asyncio.gather(*tasks)
    return [link for sublist in results for link in sublist]  # Flatten list

async def limited_extract(url, semaphore):
    """Limits concurrent calls to extract product details."""
    async with semaphore:
        return await extract_product_info(url)

async def extract_product_data(product_links: list):
    """Extracts product details concurrently from multiple product pages."""
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    tasks = [limited_extract(url, semaphore) for url in product_links]
    results = await asyncio.gather(*tasks)
    return [result for result in results if result]  # Remove failed results

async def workflow(product_name, location):
    """Runs the scraping workflow for one product and one location."""
    print(f"\n🔍 Scraping Google Search results for '{product_name}' in {location}...")
    vendor_links = await get_google_search_links(product_name, location)
    print(f"✅ Extracted {len(vendor_links)} vendor links.")

    if not vendor_links:
        print("❌ No vendor links found. Exiting workflow.")
        return

    # Split vendor links into product pages and vendor pages
    product_links = [link for link in vendor_links if "products" in link]
    vendor_pages = [link for link in vendor_links if "products" not in link]

    all_product_details = []

    if product_links:
        print("\n🔍 Extracting product details directly from search results...")
        direct_product_details = await extract_product_data(product_links)
        all_product_details.extend(direct_product_details)
        print(f"✅ Extracted {len(direct_product_details)} product details directly.")

    if vendor_pages:
        print("\n🔍 Scraping vendor pages for product links...")
        extracted_product_links = await scrape_inside_urls(vendor_pages, "https://www.tradeindia.com/products/")
        print(f"✅ Extracted {len(extracted_product_links)} product links from vendor pages.")

        if extracted_product_links:
            print("\n🔍 Extracting product details from vendor pages...")
            vendor_product_details = await extract_product_data(extracted_product_links)
            all_product_details.extend(vendor_product_details)
            print(f"✅ Extracted {len(vendor_product_details)} product details from vendor pages.")

    if all_product_details:
        df = pd.DataFrame(all_product_details).drop_duplicates(subset=['vendor_name'])

        # ✅ **Create directory structure:**
        folder_path = f"./data/{product_name}/{location}"
        os.makedirs(folder_path, exist_ok=True)  # Creates folders if they don’t exist

        # ✅ **Save file in respective folder:**
        file_path = f"{folder_path}/product_details.xlsx"
        df.to_excel(file_path, index=False)

        print(f"\n📂 Data saved to {file_path}")
    else:
        print("❌ No product details extracted. No file saved.")

async def main():
    """Sequentially run workflows for each product and each location."""
    product_names = [
    
    ]
    locations = [
    
    ]
    
    if not product_names or not locations:
        print("No product names or locations provided. Exiting.")
        return
    
    for product in product_names:
        # Clean the product name
        cleaned_product = re.sub(r'[^A-Za-z0-9 ]+', ' ', product).strip()
        for location in locations:
            await workflow(cleaned_product, location)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"⏱️ Execution Time: {execution_time:.2f} seconds")
