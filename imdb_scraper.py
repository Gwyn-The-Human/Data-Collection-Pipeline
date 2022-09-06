from ast import Return
from re import X
from selenium import webdriver
PATH = "/home/gwyn/miniconda3/condabin/chromedriver" 
driver =webdriver.Chrome (PATH) 
import time
from selenium.webdriver.common.by import By



class scraper ():


    def __init__(self):
        driver.get ("https://www.imdb.com/feature/genre/?ref_=nv_ch_gr")
        pass


    def get_links(self):

        links =[]
        images = driver.find_elements(By.CSS_SELECTOR, value= "div[class^='ninja_image']")
        for image in images:
            try: #avoids the elements with 'ninja_image' in the class name w/out 'a' tag
                a_tag = image.find_element(By.TAG_NAME, 'a') 
                link= a_tag.get_attribute ('href')
                if link not in links:#removes duplicates
                    links.append (link)
            except:
                pass
        #print (links)
        #print (len (links))
        return links

#or i could just could somehow search for ninja_image, like if ninja_image in class, append href etc.etc. 


boi= scraper()
print(boi.get_links()
)