import datetime
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
#from linkedin_scraper import Person, actions
#Fix
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

search_tag = input("ใส่ keyword ในการค้นหา : ")
output_filename = input("ชื่อไฟล์ : ")
#search_scroll = int(input("ช่วงการเลื่อนเมาส์ : "))
main_url = "https://www.sanook.com/news/tag/{}/".format(search_tag)
print(main_url)

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(main_url)

soup = BeautifulSoup(driver.page_source,'html.parser')

image_lis = []
title_lis = []
tag_lis = []
content_lis = []
time_lis = []

post_lis =  [url.find('a')['href'] for url in soup.find_all('div',{'class':'archive-post-col'})][:6]
for url in post_lis: 
    driver.get(url)
    
    title = driver.find_element(By.CSS_SELECTOR,'h1.title').text.strip() 
    title_lis.append(title)
    print(title)

    time_t = driver.find_element(By.CSS_SELECTOR,'time').text.strip() 
    print(time_t)
    time_lis.append(time_t)

    image = driver.find_element(By.CSS_SELECTOR,'source').get_attribute('srcset').strip()
    image_lis.append(image) 
    print(image)

    tag = [ tag.get_attribute('title') for tag in driver.find_elements(By.CSS_SELECTOR,'a.TagItem')]
    tag_lis.append(tag)
    print(tag)

    content = driver.find_element(By.CSS_SELECTOR,'div.ReaderWrap').text 
    content_lis.append(content)
    print(content)


    print("---------------------------------")


df = pd.DataFrame()
df['ชื่อบทความ'] = title_lis 
df['รูปภาพ'] = image_lis 
df['Time'] = time_lis
df['Tag'] = tag_lis 
df['ลิงค์บทความ'] = post_lis 
df['เนื้อหา'] = content_lis 

df.to_excel("{}.xlsx".format(output_filename))