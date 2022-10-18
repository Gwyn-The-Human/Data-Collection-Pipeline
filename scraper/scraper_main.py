#could i make it a parent class and put all those variables in __init__? and then have a child class be imdb.scraper etc etc. 

#TODO make sure raw data is being saved where it is supposed to be 

#TODO possible added features: 
    #add a search bar method (e.g for searching something on linkedin)
    #add login method from tiktok_scraper.py 
 
#TODO update setup.py deets 

#TODO add path to scraper variables to make it customisable, or make it a parameter (?)
#add the file to your folder structure inside the scraper folder so you can reference by a relative path.
#better way: use os / sys model 
#use sys to connect tot he path that that
#sys allows the code to communicate with teh operating system. 
#sys module join 

#TODO if it has already scraped the data, and it doesn't save it locally, it will still add it to teh df and upload it again; fix this? 

#TODO think about an except for if the file exists but the picture wants to save there; how does it behave?

#TODO testing running image scraper without text! 

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
import boto3
import json
import psycopg2
import pandas as pd
import os
from scraper import scraper_variables
import urllib.request
import uuid


class Scraper ():

    def __init__(self):
        self.path = "/home/gwyn/miniconda3/condabin/chromedriver" 
        self.driver = webdriver.Chrome (self.path) 
        if os.path.exists ("raw_data") == False:
            os.makedirs ("raw_data")
        self.df_batch = []
        self.image_rsc_batch = []


    def scrape (self):
        """
        The main method that combines the other methods. Should be customised for use on other websites. 

        """ 
        layer_one_links = self.get_links(scraper_variables.url, scraper_variables.parent_xpath_one, scraper_variables.child_xpath_one)#lists links to genres 
        for link in layer_one_links: #for each genre link 
            layer_two_links = self.get_links(link, scraper_variables.parent_xpath_two, scraper_variables.child_xpath_two) #lists links to pages to be scraped
            for link in layer_two_links:#for each page link

               #text 
                extracted_text = self.extract_text(link)
                self.save_text(extracted_text)
                self.add_to_df_batch(extracted_text)    
                self.upload_batch_to_rds()    
                #images 
                rscs = self._extract_images_rsc()                   
                self.save_images(extracted_text, rscs)
                #self.build_image_batch (rscs, extracted_text[0]["Friendly_ID"])
                self.upload_images_to_s3(extracted_text[0]["Friendly_ID"]) 




    def get_links(self, link, parent_xpath, child_xpath): #takes URL so it can be looped through on different pages
        """
        Gets a list of links from the specified child elements of the given parent xpath.
        
        
        Iterates through child elements of a given parent and returns list of links 
        within child elements of the given parent. If the child element has multiple
        links, only the first link is added to the returned list.
        
        Args:
            url: the url of the page you want to scrape
            parent_xpath: the xpath of the parent element that contains the child elements you want
              to scrape
            child_xpath: the xpath shared by the child elements that contain the links
        
        Returns: 
            list of links from child elements. 
        """
        links = []
        self.driver.get(link) 
        parent = self.driver.find_elements(By.XPATH, parent_xpath)
        children = parent[0].find_elements(By.XPATH, child_xpath)
        for element in children:
            a_tag = element.find_elements(By.TAG_NAME, 'a') 
            link= a_tag[0].get_attribute('href')
            links.append(link)
        return links
   


    def extract_text (self, link):
        """
        Extracts text data.
        
        Finds the text of the elements specified by the XPATHs 
        in scraper_variables.data_catagoroes file, and returns 
        them in a dictionary paired with the tags (also specified in 
        scraper_variables.data_catagories). Generates a friendly ID 
        from the extracted text, and a uuid, both of which are included 
        in the returned dictionary.  
        
        Returns:
            A dictionary of the data scraped from the page, and associated IDs, all within a list.
    """
      
        self.driver.get(link)
        compiled_data = {}
        for catagory in scraper_variables.data_catagories:
            try:
                compiled_data[catagory] = self.driver.find_element(By.XPATH, scraper_variables.data_catagories[catagory]).get_attribute("innerText")
            except NoSuchElementException:
                print (f"no {catagory} data found at {link})")
                compiled_data [catagory] = "null"
                pass
        return [self.__add_ids(compiled_data)]   ## added [] here to work with pd.read_json; 
        

    def __add_ids (self, compiled_data):
        compiled_data["Friendly_ID"] = compiled_data[list(compiled_data)[0]] + "-" + compiled_data[list(compiled_data)[1]] #uses list () to index the dictionary compiled_data
        compiled_data["UUID"] = str(uuid.uuid4())
        return compiled_data


    def _get_multiple_elements_text(self, xpath): 
        """
        Returns text in cases where one instance of text data is located accross multiple elements 
        under a single parent element. 
        
        Args:RROR:  type "year" does not exist
            xpath: (str) the xpath of the parent element

        Returns: 
            a list of strings that make up one instance of text data. 
        """
        text = []
        parent = self.driver.find_element(By.XPATH, xpath)    # def build_image_batch (self, rscs, friendly_id):###in progress
    #     if scraper_variables.scrape_images:
    #         self.image_rsc_batch.append (rscs)
    #         if len(self.image_rsc_batch) == scraper_variables.batch_size:
    #             image_path = f"raw_data/image_batch"
    #             os.makedirs(image_path)
    #             for rsc_list in self.image_rsc_batch:
    #                 for image_rsc in rsc_list:
    #                     urllib.request.urlretrieve(image_rsc, f"{image_path}/{friendly_id}.jpeg"),
        text_elements = parent.find_elements(By.TAG_NAME, "span")
        for inner_text in text_elements:
            text.append(inner_text.get_attribute("innerText"))
        return text


    def save_text(self, text_data):
        """
        Takes a dictionary of text data, and saves it in a file named after the friendly_ID
        in the raw_data directory
        
        Args:
            text_data: dictionary of the text data

        Raises:
            FileExistsError: an error occured when saving text that has already by saved. 
        """
        data_repo_path = os.path.abspath("raw_data")
        text_path = data_repo_path + "/" + text_data[0]["Friendly_ID"]   #string indeceses must be integers 
        try:
            os.makedirs(text_path) #creates a file named the friendly ID in the Raw_Data directory
            with open(text_path + "/data.json", "w") as file:
             #   print (text_data)
             #   print (json.dumps(text_data))
                file.write (json.dumps(text_data))
        except FileExistsError:
            print(f"file {text_data[0]['Friendly_ID']} already saved!") # also here added [0]


    def _extract_images_rsc(self):
        """
        Returns a list of image sources with attributes specified in scraper_variables.image_attributes
        from the page the driver is on. 
        """
        if scraper_variables.scrape_images == False:
            return None
        rsc_list = []
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        pics = soup.find_all("img", attrs = scraper_variables.image_attributes) 
        for pic in pics: #the for statement loops through pics (a list) and allows for more than one image to be scraped. 
            rsc_list.append(pic ["src"])
            if rsc_list == []:
                print ("no images found with the given attributes in scraper_variables.")
        return rsc_list

    
    def save_images(self, text_data, rsc_list):#could this be a static method? pros? cons? 
        # Still needs to access scraper_variables!! 
        """
        Takes a list of image rscs and downloads them to a folder named after the file's friendly ID
        
        Args:
            text_data: a dictionary containing the text data for the file
            rsc_list: a list of image rsc's
        """
        if scraper_variables.scrape_images:
            image_id = text_data[0]['Friendly_ID']
            image_path = f"raw_data/{image_id}/images" ## also here added [0]
            if os.path.exists(image_path) == False:
                os.makedirs(image_path)
            for pic_rsc in rsc_list:
                urllib.request.urlretrieve(pic_rsc, f"{image_path}/{image_id}.jpeg"),  #also here added [0]
   
   
    # def build_image_batch (self, rscs, friendly_id):###in progress
    #     if scraper_variables.scrape_images:
    #         self.image_rsc_batch.append (rscs)
    #         if len(self.image_rsc_batch) == scraper_variables.batch_size:
    #             image_path = f"raw_data/image_batch"
    #             os.makedirs(image_path)
    #             for rsc_list in self.image_rsc_batch:
    #                 for image_rsc in rsc_list:
    #                     urllib.request.urlretrieve(image_rsc, f"{image_path}/{friendly_id}.jpeg"),
    
   
    def upload_images_to_s3(self, file_name): #same problem as df; need to upload them all at once! 
        if scraper_variables.scrape_images and scraper_variables.upload:
             s3_client = boto3.client('s3')
             image_response = s3_client.upload_file(f'raw_data/{file_name}/images/{file_name}.jpeg', scraper_variables.bucket, file_name + ".jpeg")


    def add_to_df_batch (self,extracted_text): 
        if scraper_variables.upload:
            df= pd.DataFrame(extracted_text)
            self.df_batch.append (df)


    def upload_batch_to_rds(self):
        if scraper_variables.upload: #make these if gates cleaner
            if len (self.df_batch) == scraper_variables.batch_size:
                complete_df = pd.concat (self.df_batch) 
                complete_df = complete_df.astype ("str")
                engine = create_engine (scraper_variables.connenction_string) 
                complete_df.to_sql(scraper_variables.table_name, engine, if_exists='append') 
                self.df_batch = []


if __name__ == "__main__":
    my_scraper = Scraper()
    my_scraper.scrape()




    # def upload_text_to_RDS (self, extracted_text):
    #     with psycopg2.connect(

    #         host=scraper_variables.HOST, 
    #         user=scraper_variables.USER, 
    #         password=scraper_variables.PASSWORD, 
    #         dbname=scraper_variables.DATABASE, 
    #         port=scraper_variables.PORT
            
    #     ) as conn:
    #         with conn.cursor() as cur:
    #             cur.execute (f'''INSERT INTO test_table VALUES ( 
    #             {extracted_text["Friendly_ID"]}, {extracted_text["UUID"]}
    #             ) ''')
    #             print ("TYPE IS:")
    #             print(type(cur))
    #             conn.commit()
    #             records = cur.fetchall()


    # def next_page(self, button_XPATH): #HMMMMMMMM maybe this just needs to all go in scrape()! 
    #     counter = 0
    #     while counter < scraper_variables.number_of_nexts:
    #         try:
    #             self.driver.find_element(By.XPATH, button_XPATH).click()
    #             counter +=1
    #         except NoSuchElementException:
    #             print ("next button not found. Maybe no more pages left.")
    #             break


    #     next_button_cell= driver.find_element(By.XPATH, value= "desc")
    #     a_tag = next_button_cell.find_element(By.TAG_NAME, value= 'a')
    #     next_link = a_tag.get_attribute ('href')
    #     self.driver.get (next_link)
    #     # TODO add a while loop so it will stop scrolling once it hits the final next. 
    #     #TODO generlalise this! 
    #     #TODO is this just click
    #     extracted_text = self.extract_text (link)
    #     my_scraper.save_text (extracted_text)
    #     my_scraper.save_images (extracted_text, self._extract_images_rsc (link) )


