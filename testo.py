from operator import contains
from selenium import webdriver
PATH = "/home/gwyn/miniconda3/condabin/chromedriver" 
driver =webdriver.Chrome (PATH) 
from selenium.webdriver.common.by import By
import uuid
import os
import scraper_variables


#driver.get ("https://www.imdb.com/feature/genre/?ref_=nv_ch_gr")
#elements = driver.find_element (By.XPATH, '//*[@id="main"]/div[6]/span/div/div/div/div' )
#a_tags = elements.find_elements(By.TAG_NAME, 'a') 
#for tags in a_tags:
   # link= tags.get_attribute ('href')
    #print (link)



driver.get ("https://www.imdb.com/title/tt10648342/?ref_=adv_li_tt")

try:
    genres = driver.find_element('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[1]/a').get_attribute("innerText")
except:
    pass
print (genres)