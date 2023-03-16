from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing.pool import Pool


def urlAmazon(url=str(),paging_method=int()):
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
    url = url.format(paging_method)
    req = requests.get(url,headers=headers)
    soup = BeautifulSoup(req.content,"lxml")
    productList= soup.find("div","s-main-slot s-result-list s-search-results sg-row").findAll("div","sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20")
    if not soup.find("div","a-section a-text-center s-pagination-container"):
        exit()
    else:
        pass
    
    print(paging_method, len(productList))
    for product in productList:
        productName = product.find("h2").getText(strip=True)
        try:
            productPrice = product.find("span","a-offscreen").getText(strip=True)
        except:
            productPrice = None
        with open("products.txt","a",encoding="UTF-8") as f:
            f.write(f"{productName}: {productPrice} - {paging_method}\n")

def main(pool, loop):  
    
    page = 1  
    url = "https://www.amazon.com.tr/s?i=electronics&bbn=13709880031&rh=n%3A13709880031%2Cp_n_fulfilled_by_amazon%3A21345978031&dc&page={}&rnid=21345970031&ref=sr_pg_2"        
    while loop:
        for i in range(11,-1,-1):           
            p = pool.apply_async(func=urlAmazon,args=[url,12*page-i])                                      
        page+=1
    print("Buraya ulaştıysak bir obkluk var")
    
if __name__ == '__main__': 
    pool = Pool()
    loop = True
    start = time.perf_counter()    
    main(pool,loop)   
    finish = time.perf_counter()
    print(round(finish-start,2))
        
    
