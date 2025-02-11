# import asyncio
# from crawl4ai import AsyncWebCrawler
# from crawl_inside import fetch_tradeindia_links
# from extract_product_information import extract_product_info
# import pandas as pd
# import re
# import time
# import subprocess 


# subprocess.Popen("ulimit -n 100000", shell=True, close_fds=True)  # Increase file descriptor limit

# async def get_google_search_links(product: str, location: str, num_pages: int = 1):
#     """ Scrapes Google search results and filters only TradeIndia vendor links. """
    
#     base_google_url = "https://www.google.com/search?q=site:tradeindia.com+{}+{}&start={}"
#     base_tradeindia_url = f"https://www.tradeindia.com/{location.lower()}/"
#     formatted_product = "+".join(product.split())  
#     formatted_location = "+".join(location.split())

#     search_links = []  

#     async with AsyncWebCrawler() as crawler:
#         tasks = [
#             crawler.arun(base_google_url.format(formatted_product, formatted_location, page * 10))
#             for page in range(num_pages)
#         ]

#         results = await asyncio.gather(*tasks)

#         for result in results:
#             if result.success:
#                 search_results = result.links.get("external", [])  
#                 search_links.extend(
#                     link["href"] for link in search_results
#                     if "href" in link and link["href"].startswith(base_tradeindia_url)
#                 )
#             else:
#                 print(f"❌ Failed to scrape Google Search results: {result.error_message}")
    
#     return search_links


# async def scrape_inside_urls(inside_urls: list, tradeindia_base_url: str):
#     """ Scrapes internal product links from multiple TradeIndia vendor pages in parallel. """
#     tasks = [fetch_tradeindia_links(url, tradeindia_base_url) for url in inside_urls]
#     results = await asyncio.gather(*tasks)
#     return [link for sublist in results for link in sublist]  # Flatten list


# async def extract_product_data(product_links: list):
#     """ Extracts product details concurrently from multiple product pages. """
#     tasks = [extract_product_info(url) for url in product_links]
#     results = await asyncio.gather(*tasks)
#     return [result for result in results if result]  # Remove failed results


# async def workflow(product_name, location):
#     """ Main function to run scraping workflow in parallel. """
    
#     print(f"\n🔍 Scraping Google Search results for {product_name} in {location}...")
#     vendor_links = await get_google_search_links(product_name, location)
#     print(f"✅ Extracted {len(vendor_links)} vendor links.")

#     if not vendor_links:
#         print("❌ No vendor links found. Exiting.")
#         return

#     # Split vendor links into product pages & vendor pages
#     product_links = [link for link in vendor_links if "products" in link]
#     vendor_pages = [link for link in vendor_links if "products" not in link]

#     all_product_details = []

#     # If direct product pages exist, scrape them first (parallel)
#     if product_links:
#         print("\n🔍 Extracting product details directly from search results...")
#         direct_product_details = await extract_product_data(product_links)
#         all_product_details.extend(direct_product_details)
#         print(f"✅ Extracted {len(direct_product_details)} product details directly.")

#     # If no product links found, extract from vendor pages
#     if vendor_pages:
#         print("\n🔍 Scraping vendor pages for product links (parallel)...")
#         extracted_product_links = await scrape_inside_urls(vendor_pages, "https://www.tradeindia.com/products/")
#         print(f"✅ Extracted {len(extracted_product_links)} product links from vendor pages.")

#         if extracted_product_links:
#             print("\n🔍 Extracting product details from vendor pages (parallel)...")
#             vendor_product_details = await extract_product_data(extracted_product_links)
#             all_product_details.extend(vendor_product_details)
#             print(f"✅ Extracted {len(vendor_product_details)} product details from vendor pages.")

#     # Save results to Excel
#     if all_product_details:
#         df = pd.DataFrame(all_product_details).drop_duplicates(subset=['vendor_name'])
#         file_name = f"product_details_{product_name}_{location}.xlsx"
#         df.to_excel(file_name, index=False)
#         print(f"\n📂 Data saved to {file_name}")
#     else:
#         print("❌ No product details extracted. No file saved.")


# async def main():
#     """Sequentially run workflows for each product and each location."""
#     product_names = [
#     "HPDE DRUMS 6L",
#     "ETHYL ACETATE",
#     "TRIMETHYLSILYL-TRIFLUROMETHANESULFONATE",
#     "BACKING FLANGE WITH RUBBER CORD Size 4",
#     "SS316 BSP THREAD NIPPLE 3/4 Øx6",
#     "Aluminium bottle Anodized 5M 2L 500 T. 8"
#     "SAMPLE CONTAINER PP HDPE 100MLSTERILE",
#     "GRACE ALTIMA C18 250X4.6MM 5.0µm",
#     "ZORBAX ECLIPSE XDB-C8 4.6X150MMX5UM 9939",
#     "DISPOSABLE WEIGHING-DISH FB08732112",
#     "PRESSURE FILTER CLOTH 44 INCH DIA",
#     "GI BOLTS & NUTS HEX HEAD Size 1/2 X 1",
#     "WHITE BOARD MARKER PENS",
#     "TRIETHYL AMINE",
#     "STERILE PETRIDESH DISPOSABLE 90MM",
#     "WRINGLER BUCKET RY-24 466L MOP",
#     "SOYABEAN CASEIN DIGEST MEDIUM 100ML",
#     "FMOC-D-THR OTBU OH CASNO 138797-71-4",
#     "LYPHILIZE RBF S N 1000ML 24 40 WITH HUCK",
#     "ACETONITRILE ULC MS GRADE",
#     "ORION ROSS ULTRA FLAT PH ELECTRODE",
#     "GI HEX HEAD NUT 5/16 BSW",
#     "TLC PLATES",
#     "Dimethyl Sulfoxide GC Grade",
#     "N-NITROSODIETHYLAMINE NDEA",
#     "SS316BALL VALVE F E ASA-150 Size 1 1/2",
#     "FLAT ORDINERY FILES WITH NEULAND ADDERS",
#     "AUTOCLAVABLE DISPOSABLE POLYTHENE BAGS",
#     "SODIUM SALICYLATE-AR",
#     "CHIRALCEL OJ-H 250X4.6MMX5MICRON",
#     "POLYTHENE SHEET SIZE 22 X38 ANTI STATIC",
#     "Soyabean-Casein Digest Agar MH290",
#     "X-Bridge C18 150X4.6mmx3.5um",
#     "STORE REQUISITION SLIP BOOKS 1/8 SIZE 1",
#     "QC FORMAT REGISTERS 200 PAGES A4 SIZE",
#     "SOYABEAN CASEIN DIGEST AGAR",
#     "QC FORMAT REGISTERS 200 PAGES A3 SIZE",
#     "OE350 - UNITEC T -BAR GREEN 35 CM",
#     "GI HEX HEAD NUT 3/8 BSW",
#     "Ladies Shoes",
#     "P.P.PALLETS SIZE 1200X1200 MM",
#     "LIMULUS AMOEBOCYTE LYSATE",
#     "CAFFEINE USP REF STDCAT NO 1085003",
#     "TETRAPROPYL AMMONIUM CHLORIDE",
#     "NUT WITH SLIT M5 P/N 221-32705",
#     "CAPILLARY ADAPTER 221-45816-01",
#     "BARIUM HYDROXIDE AR",
#     "2ML LCMS VIALS WATERS 186000307C",
#     "ORTHOPHOSPHORIC ACID AR GRADE MAKE MERCK",
#     "QC FORMAT REGISTERS 100 PAGES A4 SIZE",
#     "YELLOW PAPERS A4",
#     "MAGNESIUM NITRATE",
#     "HOT WORK PERMIT BOOKS 1+1 IN A SET 100SET",
#     "GI BOLTS & NUTS HEX HEAD Size 3/8 X 2",
#     "GI HEX HEAD BOLTS BSW 5/8 X6",
#     "GC Syringe 10µL",
#     "LYPHILIZE RBF S N 2000ML 24 40 WITH HUCK",
#     "SS304 BALL VALVE F E ASA-150 SIZE 2",
#     "4-(4-NITROPHENYL)-3-MORPHOLINONE 446292",
#     "Palmitic Acid",
#     "ANALYTICAL TEST REQUISITION PAD",
#     "Volumetric Flask 200ML Class-A",
#     "METHANOL ULC MS-SF GRADE",
#     "MOBILE PHASE BOTTLES 5LTR",
#     "DEPYROGENATED TUBES 13x100 mm",
#     "MICRO WELL STAND",
#     "PVC BARREL PUMP 220 L CAP MODEL-SPH/3",
#     "LEAF FILTER BAGS BIG SIZE",
#     "CEMENT BAGS EMPTY",
#     "SILVER VINYLE LABELS 5.75 X3.5",
#     "HYDROGEN GAS CYL GRADE-1 PURITY 99.999%",
#     "GI BOLTS & NUTS HEX HEAD Size 3/8 X 1",
#     "16Dia SS316 Stand Rod With C.I Base 6kg",
#     "V-BELTS B 68",
#     "TOLUENE",
#     "DISPOSABLE STERILE MEDIA BOTTLES 250 ML",
#     "4-(3-AMINOPHENYL)MORPHOLIN-3-ONE 1082495",
#     "1-BROMO-3-METHOXY PROPANE CAS 36865-41-5",
#     "DIMETHYL SULFOXIDE-D6 ML",
#     "DIMETHYL FORMAMIDE",
#     "DAILY PERFORMANCE CHECK BOOKS",
#     "MONTHLY CALIBRATION BOOKS",
#     "GI BOLTS & NUTS HEX HEAD Size 1/2 X 2",
#     "200µl CLEAR INDIVIDUAL PEAL OFF PLASTIC",
#     "NEOPRINE HAND GLOVES",
#     "PH METER LP-139SA",
#     "LYPHILIZE RBF S N 500ML 24 40 WITH HUCK",
#     "SP 18MLVIAL G3160-65304",
#     "10X75MM DIA DEPYROGENATED TEST TUBES",
#     "SILICON GASKET 290X125 MAKE NEWTRONIC",
#     "429415-L-A-LECITHIN SOYBEAN 8002-43-5",
#     "GI Hexagonal Head Nut-3/4 BSW",
#     "GI Hexagonal Head Nut-5/8 BSW",
#     "GI Hexagonal Head Nut-1/2 BSW",
#     "WHITE APRONS",
#     "LAB STIRRER LS-5 DRILL CHUCK & SPEED CON",
#     "SULFURIC ACID 94-98 percentage FOR TRACE METAL ANALYSIS",
#     "Rivaroxaban related comp-B",
#     "TETRABENZYL PYROPHOSPHATE 990-91-0",
#     "ETHYL ACETATE",
#     "SS316 HEX HEAD BOLT&NUT BSW 3/8 X3",
#     "SS316 BOLT HEX HEAD M10X70MM",
#     "2-NITRO-5-BROMOPYRIDINE CAS 39856-50-3",
#     "GI Hex Head Bolt 5/8 BSW X3",
#     "LAB CHAIRS",
#     "STANNOL PURE",
#     "N-NITROSODIMETHYLAMINE NDMA",
#     "Rivaroxaban related comp-J",
#     "Rink amide MBHA resin CAS 431041-83-7",
#     "CO2 CYLINDER HORNS",
#     "ISOPROPYL ALCOHOL",
#     "Rivaroxaban related comp-D",
#     "ISSUANCE REGISTER",
#     "TEFLON GLAND",
#     "BACKING FLANGE WITH RUBBERCORD Size 1",
#     "MAGNETIC STIRRER WITH HOTPLATE MS-2 MODEL"
#     ]
#     locations = [
#         "Mumbai",
#         "Delhi",
#         "Chennai",
#         "Bangalore",
#         "Hyderabad",
#         "Ahmedabad",
#         "Pune",
#         "Surat",
#         "Kolkata",
#         "Coimbatore",
#         "Vadodara",
#         "Jaipur",
#         "Nagpur",
#         "Lucknow",
#         "Indore"
#     ]

#     # Clean product names
#     cleaned_product_names = [re.sub(r'[^A-Za-z0-9 ]+', ' ', p).strip() for p in product_names]
    
#     # Run each workflow sequentially
#     for product in cleaned_product_names:
#         for location in locations:
#             await workflow(product, location)


# if __name__ == "__main__":
#     start_time = time.time()
#     asyncio.run(main())
#     end_time = time.time()
#     execution_time = end_time - start_time
#     print(f"Execution Time: {execution_time:.5f} seconds")
# # need to done
# """  
# "SINGLE USE DATALOGGER TEMP -30 DEG TO 70",
#     "HPDE DRUMS 6L",
#     "ETHYL ACETATE",
#     "TRIMETHYLSILYL-TRIFLUROMETHANESULFONATE",
#     "BACKING FLANGE WITH RUBBER CORD Size 4",
#     "SS316 BSP THREAD NIPPLE 3/4 Øx6",
#     "Aluminium bottle Anodized 5M 2L 500 T. 8"
#     "SAMPLE CONTAINER PP HDPE 100MLSTERILE",
#     "GRACE ALTIMA C18 250X4.6MM 5.0µm",
#     "ZORBAX ECLIPSE XDB-C8 4.6X150MMX5UM 9939",
#     "DISPOSABLE WEIGHING-DISH FB08732112",
#     "PRESSURE FILTER CLOTH 44 INCH DIA",
#     "GI BOLTS & NUTS HEX HEAD Size 1/2 X 1",
#     "WHITE BOARD MARKER PENS",
#     "TRIETHYL AMINE",
#     "STERILE PETRIDESH DISPOSABLE 90MM",
#     "WRINGLER BUCKET RY-24 466L MOP",
#     "SOYABEAN CASEIN DIGEST MEDIUM 100ML",
#     "FMOC-D-THR OTBU OH CASNO 138797-71-4",
#     "LYPHILIZE RBF S N 1000ML 24 40 WITH HUCK",
#     "ACETONITRILE ULC MS GRADE",
#     "ORION ROSS ULTRA FLAT PH ELECTRODE",
#     "GI HEX HEAD NUT 5/16 BSW",
#     "TLC PLATES",
#     "Dimethyl Sulfoxide GC Grade",
#     "N-NITROSODIETHYLAMINE NDEA",
#     "SS316BALL VALVE F E ASA-150 Size 1 1/2",
#     "FLAT ORDINERY FILES WITH NEULAND ADDERS",
#     "AUTOCLAVABLE DISPOSABLE POLYTHENE BAGS",
#     "SODIUM SALICYLATE-AR",
#     "CHIRALCEL OJ-H 250X4.6MMX5MICRON",
#     "POLYTHENE SHEET SIZE 22 X38 ANTI STATIC",
#     "Soyabean-Casein Digest Agar MH290",
#     "X-Bridge C18 150X4.6mmx3.5um",
#     "STORE REQUISITION SLIP BOOKS 1/8 SIZE 1",
#     "QC FORMAT REGISTERS 200 PAGES A4 SIZE",
#     "SOYABEAN CASEIN DIGEST AGAR",
#     "QC FORMAT REGISTERS 200 PAGES A3 SIZE",
#     "OE350 - UNITEC T -BAR GREEN 35 CM",
#     "GI HEX HEAD NUT 3/8 BSW",
#     "Ladies Shoes",
#     "P.P.PALLETS SIZE 1200X1200 MM",
#     "LIMULUS AMOEBOCYTE LYSATE",
#     "CAFFEINE USP REF STDCAT NO 1085003",
#     "TETRAPROPYL AMMONIUM CHLORIDE",
#     "NUT WITH SLIT M5 P/N 221-32705",
#     "CAPILLARY ADAPTER 221-45816-01",
#     "BARIUM HYDROXIDE AR",
#     "2ML LCMS VIALS WATERS 186000307C",
#     "ORTHOPHOSPHORIC ACID AR GRADE MAKE MERCK",
#     "QC FORMAT REGISTERS 100 PAGES A4 SIZE",
#     "YELLOW PAPERS A4",
#     "MAGNESIUM NITRATE",
#     "HOT WORK PERMIT BOOKS 1+1 IN A SET 100SET",
#     "GI BOLTS & NUTS HEX HEAD Size 3/8 X 2",
#     "GI HEX HEAD BOLTS BSW 5/8 X6",
#     "GC Syringe 10µL",
#     "LYPHILIZE RBF S N 2000ML 24 40 WITH HUCK",
#     "SS304 BALL VALVE F E ASA-150 SIZE 2",
#     "4-(4-NITROPHENYL)-3-MORPHOLINONE 446292",
#     "Palmitic Acid",
#     "ANALYTICAL TEST REQUISITION PAD",
#     "Volumetric Flask 200ML Class-A",
#     "METHANOL ULC MS-SF GRADE",
#     "MOBILE PHASE BOTTLES 5LTR",
#     "DEPYROGENATED TUBES 13x100 mm",
#     "MICRO WELL STAND",
#     "PVC BARREL PUMP 220 L CAP MODEL-SPH/3",
#     "LEAF FILTER BAGS BIG SIZE",
#     "CEMENT BAGS EMPTY",
#     "SILVER VINYLE LABELS 5.75 X3.5",
#     "HYDROGEN GAS CYL GRADE-1 PURITY 99.999%",
#     "GI BOLTS & NUTS HEX HEAD Size 3/8 X 1",
#     "16Dia SS316 Stand Rod With C.I Base 6kg",
#     "V-BELTS B 68",
#     "TOLUENE",
#     "DISPOSABLE STERILE MEDIA BOTTLES 250 ML",
#     "4-(3-AMINOPHENYL)MORPHOLIN-3-ONE 1082495",
#     "1-BROMO-3-METHOXY PROPANE CAS 36865-41-5",
#     "DIMETHYL SULFOXIDE-D6 ML",
#     "DIMETHYL FORMAMIDE",
#     "DAILY PERFORMANCE CHECK BOOKS",
#     "MONTHLY CALIBRATION BOOKS",
#     "GI BOLTS & NUTS HEX HEAD Size 1/2 X 2",
#     "200µl CLEAR INDIVIDUAL PEAL OFF PLASTIC",
#     "NEOPRINE HAND GLOVES",
#     "PH METER LP-139SA",
#     "LYPHILIZE RBF S N 500ML 24 40 WITH HUCK",
#     "SP 18MLVIAL G3160-65304",
#     "10X75MM DIA DEPYROGENATED TEST TUBES",
#     "SILICON GASKET 290X125 MAKE NEWTRONIC",
#     "429415-L-A-LECITHIN SOYBEAN 8002-43-5",
#     "GI Hexagonal Head Nut-3/4 BSW",
#     "GI Hexagonal Head Nut-5/8 BSW",
#     "GI Hexagonal Head Nut-1/2 BSW",
#     "WHITE APRONS",
#     "LAB STIRRER LS-5 DRILL CHUCK & SPEED CON",
#     "SULFURIC ACID 94-98 percentage FOR TRACE METAL ANALYSIS",
#     "Rivaroxaban related comp-B",
#     "TETRABENZYL PYROPHOSPHATE 990-91-0",
#     "ETHYL ACETATE",
#     "SS316 HEX HEAD BOLT&NUT BSW 3/8 X3",
#     "SS316 BOLT HEX HEAD M10X70MM",
#     "2-NITRO-5-BROMOPYRIDINE CAS 39856-50-3",
#     "GI Hex Head Bolt 5/8 BSW X3",
#     "LAB CHAIRS",
#     "STANNOL PURE",
#     "N-NITROSODIMETHYLAMINE NDMA",
#     "Rivaroxaban related comp-J",
#     "Rink amide MBHA resin CAS 431041-83-7",
#     "CO2 CYLINDER HORNS",
#     "ISOPROPYL ALCOHOL",
#     "Rivaroxaban related comp-D",
#     "ISSUANCE REGISTER",
#     "TEFLON GLAND",
#     "BACKING FLANGE WITH RUBBERCORD Size 1",
#     "MAGNETIC STIRRER WITH HOTPLATE MS-2 MODEL",

# """
import asyncio
import os
import pandas as pd
import re
import time
import subprocess
from crawl4ai import AsyncWebCrawler
from crawl_inside import fetch_tradeindia_links
from extract_product_information import extract_product_info
import random

# Increase file descriptor limit
subprocess.Popen("ulimit -n 100000", shell=True, close_fds=True)

CONCURRENCY_LIMIT = 7

async def limited_arun(crawler, url, semaphore):
    """Limits the number of concurrent web scraping requests."""
    async with semaphore:
        return await crawler.arun(url)

async def get_google_search_links(product: str, location: str, num_pages: int = 10):
    """Scrapes Google search results and filters only TradeIndia vendor links."""
    base_google_url = "https://www.google.com/search?q=site:tradeindia.com+{}+{}&start={}"
    formatted_product = "+".join(product.split())
    formatted_location = "+".join(location.split())
    search_links = []
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    async with AsyncWebCrawler(headers=headers) as crawler:
        tasks = [
            limited_arun(crawler, base_google_url.format(formatted_product, formatted_location, page * 10), semaphore)
            for page in range(num_pages)
        ]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result.success:
                search_results = result.links.get("external", [])
                # print("Raw search results:", search_results)  # Debugging
#
                search_links.extend(
                    link["href"] for link in search_results if isinstance(link, dict) and "href" in link
                )
            else:
                print(f"❌ Failed to scrape Google: {result.error_message}")
            await asyncio.sleep(random.uniform(2, 5))  # Prevent IP bans

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
     "HPDE DRUMS 6L",
     "ETHYL ACETATE",
     "TRIMETHYLSILYL-TRIFLUROMETHANESULFONATE",
     "BACKING FLANGE WITH RUBBER CORD Size 4",
     "SS316 BSP THREAD NIPPLE 3/4 Øx6",
     "Aluminium bottle Anodized 5M 2L 500 T. 8"
     "SAMPLE CONTAINER PP HDPE 100MLSTERILE",
     "GRACE ALTIMA C18 250X4.6MM 5.0µm",
     "ZORBAX ECLIPSE XDB-C8 4.6X150MMX5UM 9939",
     "DISPOSABLE WEIGHING-DISH FB08732112",
     "PRESSURE FILTER CLOTH 44 INCH DIA",
     "GI BOLTS & NUTS HEX HEAD Size 1/2 X 1",
     "WHITE BOARD MARKER PENS",
     "TRIETHYL AMINE",
     "STERILE PETRIDESH DISPOSABLE 90MM",
     "WRINGLER BUCKET RY-24 466L MOP",
     "SOYABEAN CASEIN DIGEST MEDIUM 100ML",
     "FMOC-D-THR OTBU OH CASNO 138797-71-4",
     "LYPHILIZE RBF S N 1000ML 24 40 WITH HUCK",
     "ACETONITRILE ULC MS GRADE",
     "ORION ROSS ULTRA FLAT PH ELECTRODE",
     "GI HEX HEAD NUT 5/16 BSW",
     "TLC PLATES",
     "Dimethyl Sulfoxide GC Grade",
     "N-NITROSODIETHYLAMINE NDEA",
     "SS316BALL VALVE F E ASA-150 Size 1 1/2",
     "FLAT ORDINERY FILES WITH NEULAND ADDERS",
     "AUTOCLAVABLE DISPOSABLE POLYTHENE BAGS",
     "SODIUM SALICYLATE-AR",
     "CHIRALCEL OJ-H 250X4.6MMX5MICRON",
     "POLYTHENE SHEET SIZE 22 X38 ANTI STATIC",
     "Soyabean-Casein Digest Agar MH290",
     "X-Bridge C18 150X4.6mmx3.5um",
     "STORE REQUISITION SLIP BOOKS 1/8 SIZE 1",
     "QC FORMAT REGISTERS 200 PAGES A4 SIZE",
     "SOYABEAN CASEIN DIGEST AGAR",
     "QC FORMAT REGISTERS 200 PAGES A3 SIZE",
     "OE350 - UNITEC T -BAR GREEN 35 CM",
     "GI HEX HEAD NUT 3/8 BSW",
     "Ladies Shoes",
     "P.P.PALLETS SIZE 1200X1200 MM",
     "LIMULUS AMOEBOCYTE LYSATE",
     "CAFFEINE USP REF STDCAT NO 1085003",
     "TETRAPROPYL AMMONIUM CHLORIDE",
     "NUT WITH SLIT M5 P/N 221-32705",
     "CAPILLARY ADAPTER 221-45816-01",
     "BARIUM HYDROXIDE AR",
     "2ML LCMS VIALS WATERS 186000307C",
     "ORTHOPHOSPHORIC ACID AR GRADE MAKE MERCK",
     "QC FORMAT REGISTERS 100 PAGES A4 SIZE",
     "YELLOW PAPERS A4",
     "MAGNESIUM NITRATE",
     "HOT WORK PERMIT BOOKS 1+1 IN A SET 100SET",
     "GI BOLTS & NUTS HEX HEAD Size 3/8 X 2",
     "GI HEX HEAD BOLTS BSW 5/8 X6",
     "GC Syringe 10µL",
     "LYPHILIZE RBF S N 2000ML 24 40 WITH HUCK",
     "SS304 BALL VALVE F E ASA-150 SIZE 2",
     "4-(4-NITROPHENYL)-3-MORPHOLINONE 446292",
     "Palmitic Acid",
     "ANALYTICAL TEST REQUISITION PAD",
     "Volumetric Flask 200ML Class-A",
     "METHANOL ULC MS-SF GRADE",
     "MOBILE PHASE BOTTLES 5LTR",
     "DEPYROGENATED TUBES 13x100 mm",
     "MICRO WELL STAND",
     "PVC BARREL PUMP 220 L CAP MODEL-SPH/3",
     "LEAF FILTER BAGS BIG SIZE",
     "CEMENT BAGS EMPTY",
     "SILVER VINYLE LABELS 5.75 X3.5",
     "HYDROGEN GAS CYL GRADE-1 PURITY 99.999%",
     "GI BOLTS & NUTS HEX HEAD Size 3/8 X 1",
     "16Dia SS316 Stand Rod With C.I Base 6kg",
     "V-BELTS B 68",
     "TOLUENE",
     "DISPOSABLE STERILE MEDIA BOTTLES 250 ML",
     "4-(3-AMINOPHENYL)MORPHOLIN-3-ONE 1082495",
     "1-BROMO-3-METHOXY PROPANE CAS 36865-41-5",
     "DIMETHYL SULFOXIDE-D6 ML",
     "DIMETHYL FORMAMIDE",
     "DAILY PERFORMANCE CHECK BOOKS",
     "MONTHLY CALIBRATION BOOKS",
     "GI BOLTS & NUTS HEX HEAD Size 1/2 X 2",
     "200µl CLEAR INDIVIDUAL PEAL OFF PLASTIC",
     "NEOPRINE HAND GLOVES",
     "PH METER LP-139SA",
     "LYPHILIZE RBF S N 500ML 24 40 WITH HUCK",
     "SP 18MLVIAL G3160-65304",
     "10X75MM DIA DEPYROGENATED TEST TUBES",
     "SILICON GASKET 290X125 MAKE NEWTRONIC",
     "429415-L-A-LECITHIN SOYBEAN 8002-43-5",
     "GI Hexagonal Head Nut-3/4 BSW",
     "GI Hexagonal Head Nut-5/8 BSW",
     "GI Hexagonal Head Nut-1/2 BSW",
     "WHITE APRONS",
     "LAB STIRRER LS-5 DRILL CHUCK & SPEED CON",
     "SULFURIC ACID 94-98 percentage FOR TRACE METAL ANALYSIS",
     "Rivaroxaban related comp-B",
     "TETRABENZYL PYROPHOSPHATE 990-91-0",
     "ETHYL ACETATE",
     "SS316 HEX HEAD BOLT&NUT BSW 3/8 X3",
     "SS316 BOLT HEX HEAD M10X70MM",
     "2-NITRO-5-BROMOPYRIDINE CAS 39856-50-3",
     "GI Hex Head Bolt 5/8 BSW X3",
     "LAB CHAIRS",
     "STANNOL PURE",
     "N-NITROSODIMETHYLAMINE NDMA",
     "Rivaroxaban related comp-J",
     "Rink amide MBHA resin CAS 431041-83-7",
     "CO2 CYLINDER HORNS",
     "ISOPROPYL ALCOHOL",
     "Rivaroxaban related comp-D",
     "ISSUANCE REGISTER",
     "TEFLON GLAND",
     "BACKING FLANGE WITH RUBBERCORD Size 1",
     "MAGNETIC STIRRER WITH HOTPLATE MS-2 MODEL"
     ]
    locations = [
    " "
    ]
    
    if not product_names or not locations:
        print("No product names or locations provided. Exiting.")
        return
    done = os.listdir("./data")
    
    for product in product_names:
        # Clean the product name
        cleaned_product = re.sub(r'[^A-Za-z0-9 ]+', ' ', product).strip()
        if cleaned_product not in done:
            for location in locations:
                await workflow(cleaned_product, location)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"⏱️ Execution Time: {execution_time:.2f} seconds")

    # links = asyncio.run(get_google_search_links("HPDE DRUMS 6L", "india"))
    # for i in links:
    #     print(i)