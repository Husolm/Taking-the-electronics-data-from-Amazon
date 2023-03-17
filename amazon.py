from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing.pool import Pool


def urlAmazon(paging_method=int()):
    url = "https://www.amazon.com.tr/s?i=electronics&bbn=13709880031&rh=n%3A13709880031%2Cp_n_fulfilled_by_amazon%3A21345978031&dc&page={paging_method}&rnid=21345970031&ref=sr_pg_2"

    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

    req = requests.get(url,headers=headers)
    soup = BeautifulSoup(req.content,"lxml")
    
    productList= soup.find("div","s-main-slot s-result-list s-search-results sg-row").findAll("div","sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20")
    
    """if not soup.find("div","a-section a-text-center s-pagination-container"):
        exit()
    else:
        pass"""
    
    print(paging_method, len(productList))
    for product in productList:
        productName = product.find("h2").getText(strip=True)
        try:
            productPrice = product.find("span","a-offscreen").getText(strip=True)
        except:
            productPrice = None
        with open("products.txt","a",encoding="utf-8") as f:
            f.write(f"{productName}: {productPrice} - {paging_method}\n")

def main():
    page_method = list(range(1,401)) # must be changed
    with Pool(50) as p: # process amount per sec
        p.map(urlAmazon, page_method) # processes loop 

    print("Finished.")
    
if __name__ == '__main__': 
    start = time.perf_counter()    
    main()  
    finish = time.perf_counter()
    print(round(finish-start,2))