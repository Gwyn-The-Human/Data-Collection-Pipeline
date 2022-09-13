from selenium import webdriver
PATH = "/home/gwyn/miniconda3/condabin/chromedriver" #where the driver is saved
driver =webdriver.Chrome (PATH) # have to download a deiver seperatly to selenium and make sure its in python path
import time
from selenium.webdriver.common.by import By


driver.get("https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list")
time.sleep (2)


try:
    driver.switch_to_frame('gdpr-consent-notice') # This is the id of the frame
    accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="save"]')
    accept_cookies_button.click()

except AttributeError: # If you have the latest version of Selenium, the code above won't run because the "switch_to_frame" is deprecated
    driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
    accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="save"]')
    #accept_cookies_button.click()

except:
    pass # If there is no cookies button, we won't find it, so we can pass

house_property = driver.find_element(by=By.XPATH, value='//*[@id="listing_62330008"]') # Change this xpath with the xpath the current page has in their properties
a_tag = house_property.find_element(By.TAG_NAME, 'a') # work out what this takes
link = a_tag.get_attribute('href')
print ("link is")
print(link)



#Blairs advice on doing social media
#ts been done but 1. more complicated and 2 (they might block you) try twitter; insta was struggle; tictoc--> maybe google how to datacscarep tictoc	
#robots.text on every website that will tell you what you are allowed to scrape