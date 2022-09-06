from ast import Return
from selenium import webdriver
PATH = "/home/gwyn/miniconda3/condabin/chromedriver" 
driver =webdriver.Chrome (PATH) 
import time
from selenium.webdriver.common.by import By




class scraper ():


    def __init__(self):
        driver.get ("https://www.tiktok.com/foryou?is_copy_url=1&is_from_webapp=v1")
        pass

    def login (self, user, password):
        ''' 
        This first has to check if somebody is already logged in and log them out, then take them to the login page and log in
        go to home

        try : logout
            then go to page 
            and log in
        
        except (if there is no logout option--> profile)
            then go to the page anyway 
            log in  

        '''
        
        try: #tests if the login button is available
            login_button = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div[1]/div/div[2]/button')

        except: #if not, logs out
            # should logout HERE
            pass

        driver.get ("https://www.tiktok.com/login/phone-or-email/email") #goes to email login and logs in. 
        username_entry = driver.find_element(by=By.XPATH, value= '//*[@id="loginContainer"]/div[1]/form/div[1]/input')
        username_entry.send_keys (user)
        password_entry = driver.find_element(by=By.XPATH, value='//*[@id="loginContainer"]/div[1]/form/div[2]/div/input')
        password_entry.send_keys (password)
        password_entry.send_keys (u'\ue007')

    def next_video (self): #only to be used after view_details
        next_button = driver.find_element (by=By.XPATH, value ='//*[@id="app"]/div[2]/div[3]/div[1]/button[3]')
        next_button.send_keys (u'\ue015')
        time.sleep (26)

    def view_details (self):
        comments_button = driver.find_element (by=By.XPATH, value= '//*[@id="app"]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[2]/button[2]')
        comments_button.click()

    #def watch_video (self): # not needed
        #pass

skoop = scraper ()
#skoop.login ('tremblebeforenebulon98@gmail.com', 'Tiktok69!')
skoop.view_details()
time.sleep (30)
skoop.next_video()