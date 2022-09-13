
from selenium import webdriver
PATH = "/home/gwyn/miniconda3/condabin/chromedriver" 
driver =webdriver.Chrome (PATH) 
import time
from selenium.webdriver.common.by import By
import uuid
import os



class scraper ():


    def __init__(self):
        driver.get ('https://www.imdb.com/feature/genre/?ref_=nv_ch_gr')
        if os.path.exists ("raw_data_test") == False:
            os.makedirs ("raw_data_test")
        
       



    def get_genre_links(self): #gets a list of genre cagories
        genre_links =[]
        images = driver.find_elements(By.CSS_SELECTOR, value= "div[class^='ninja_image']")
        for image in images:
            try: #avoids the elements with 'ninja_image' in the class name w/out 'a' tag
                a_tag = image.find_element(By.TAG_NAME, 'a') 
                link= a_tag.get_attribute ('href')
                if link not in genre_links:#removes duplicates
                    genre_links.append (link)
            except: # TODO state the specific error I'm expecting, just in case <3 
                pass
        return genre_links
    



    def scrape (self): 
        film_links = driver.find_elements(By.CLASS_NAME, value= 'lister-item mode-advanced') #generates a list of links to the films the given page 
        for film in film_links:
            text_data = self.extract_text(film)
            self.save_data(text_data)




    def save_data(self, data):
            data_repo_path = os.path.abspath("raw_data_test")
            product_path = data_repo_path + "/" + data ["Friendly ID"]   
            try:
                os.makedirs (product_path) #made a file named the friendly ID in the Raw_Data_Test directory
                with open (product_path+ "/data.json" , "w") as file:
                    file.write (str(data))
            except FileExistsError:
                print ("file already saved!")

            #self.extract_image (film)




    def extract_text (self, film):
        
        driver.get (film)
        genre = self.get_genre ()
        title =  driver.find_element(By.XPATH, value='/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1').get_attribute('innerText') #sc-b73cd867-0 eKrKux
        rating = driver.find_element(By.XPATH, value='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]').get_attribute('innerText') 
        number_of_ratings = driver.find_element(By.XPATH, value= '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/div/div/div[2]/div[3]').get_attribute('innerText') #]driver.find_element(By.CLASS_NAME, value= 'sc-7ab21ed2-3 dPVcnq').text
        date_and_type = self.date_check ()
        text_data = {

            'Title':title,
            'Date': date_and_type ['Date'],
            'Genre': genre,
            'Rating': rating,
            'Number of Ratings': number_of_ratings,
            'TV or Film':date_and_type ['Type'],
            'Friendly ID' : title + "-" + date_and_type ['Date'] + "-" +number_of_ratings, 
            'UUID': str(uuid.uuid4())
            }


        return text_data




    def date_check(self): 
        """
        IMDB pages are formatted differently for TV and films; if its a film, the date is shown first. But if it is TV, the 
        TV tag will replace the date, and the date will come second. This function checks the element that shows either 
        Date, or the TV tag:
        1-If the element is a date: returns the date and the tag 'Film'
        2-if the element is the Tag 'TV', searches for and returns the date, along with the tag 'TV' 
        
        """
        

        element = driver.find_element(By.XPATH, value='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[1]  ').get_attribute('innerText')
        print (element)
        if element == 'TV Series': 
            date =  driver.find_element(By.XPATH, value='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[2]/span').get_attribute('innerText')
            return {'Date': date, 'Type': "TV Series" }

        else: 
            return {'Date': element, 'Type': 'Film'}




    def get_genre(self): # TODO be CONSISTENT, dont use CSS_SELECTOR just randomly here! 
       
        genre = []
        genre_buttons = driver.find_elements(By.CSS_SELECTOR, "a[class^='sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt']")     #WHY DOES THIS WORK BUT BY CLASS DOESNT!!! (returns [])
        for genre_button in genre_buttons:
            span_tag = genre_button.find_element(By.TAG_NAME, 'span')
            genre.append (span_tag.get_attribute ('innerText'))
        return genre




    #def extract_image (self, film):
        #driver.get(film) 




    def scroll_to_bottom (self):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    


    
    def next_page (self):
        next_button_cell= driver.find_element(By.CLASS_NAME, value= "desc")
        a_tag = next_button_cell.find_element(By.TAG_NAME, value= 'a')
        next_link = a_tag.get_attribute ('href')
        driver.get (next_link)
        # TODO add a while loop so it will stop scrolling once it hits the final next. 



if __name__ == "__main__":
    my_scraper = scraper()
    #print(my_scraper.extract_text ('https://www.imdb.com/title/tt0093773/?ref_=adv_li_tt')) #test 
    my_scraper.save_data ({"Friendly ID":"69"})