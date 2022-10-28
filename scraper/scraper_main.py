
# possible features to add: 
    #add a search bar method (e.g for searching something on linkedin)
    #add login method from tiktok_scraper.py 
 
#TODO update setup.py deets 

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
import argparse
import boto3
import json
import os
import pandas as pd
import scraper_variables
import urllib.request
import uuid
from webdriver_manager.chrome import ChromeDriverManager #make sure my chrome is up to date! 


class Scraper():

    def __init__(self):
        #adds flag for running headless mode
        option = None
        parser = argparse.ArgumentParser()
        parser.add_argument("-hdls", "--headless", help="run the scraper as headless",
                            action="store_true")
        args = parser.parse_args()
        if args.headless:
            option = Options()
            option.headless = True 

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')

        #sets up driver, prepares raw data folder and df_batch list
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=option, chrome_options=chrome_options)
        if os.path.exists ("raw_data") == False:
            os.makedirs ("raw_data")
        self.df_batch = []


    def scrape (self):
        """
        The main method that combines the other methods. Should be customised for use on websites other than imdb. 
        """ 
        layer_one_links = self.get_links(scraper_variables.url, scraper_variables.parent_xpath_one, scraper_variables.child_xpath_one)#lists links to genres 
        for link in layer_one_links: #on imdb, for each genre link 
            layer_two_links = self.get_links(link, scraper_variables.parent_xpath_two, scraper_variables.child_xpath_two) #lists links to pages to be scraped
            for link in layer_two_links:#for each page link
               #text 
                extracted_text = self._extract_text(link)
                self._save_text(extracted_text)
                # self._add_to_df_batch(extracted_text)   #COMMENTED OUT FOR DOCKER IMAGE
                # self._upload_batch_to_rds()    #COMMENTED OUT FOR DOCKER IMAGE
                #images 
                rscs = self._extract_images_rsc()                   
                self._save_images(extracted_text, rscs)
                #self._upload_images_to_s3(extracted_text[0]["Friendly_ID"]) #COMMENTED OUT FOR DOCKER IMAGE


    def get_links(self, link: str, parent_xpath: str, child_xpath: str): #takes URL so it can be looped through on different pages
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
   

    def _extract_text (self, link: str):
        """
        Extracts text data from website.
        
        Finds the text of the elements specified by the XPATHs 
        in scraper_variables.data_catagories, and returns 
        them in a dictionary paired with the tags (also specified in 
        scraper_variables.data_catagories), all within a list. Calls 
        __ad_ids, which generates a friendly ID from the extracted 
        text, and a uuid, both of which are included in the returned
         dictionary.   
        
        Returns:
            list containing a single dictionary of the data scraped from the page, and associated IDs, all within a list.
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
        return [self.__add_ids(compiled_data)]   ## added [] around compiled data to work with pd.read_json; 
        

    def __add_ids (self, compiled_data: dict):
        """
        Takes a dictionary of data, adds IDs as two new keys to the dictionary, and returns the
        dictionary
        
        Args:
            compiled_data: the dataframe that is being passed in

        Return: 
            The compiled_data dictionary is being returned with added ID's.
        """
        compiled_data["Friendly_ID"] = compiled_data[list(compiled_data)[0]] + "-" + compiled_data[list(compiled_data)[1]] #uses list () to index the dictionary compiled_data
        compiled_data["UUID"] = str(uuid.uuid4())
        return compiled_data


    def _get_multiple_elements_text(self, xpath: str): 
        """
        Returns text in cases where one instance of text data is located accross multiple elements 
        under a single parent element. 
        
        Args:
            xpath: (str) the xpath of the parent element

        Returns: 
            a list of strings that make up one instance of text data. 
        """
        text = []
        parent = self.driver.find_element(By.XPATH, xpath)   
        text_elements = parent.find_elements(By.TAG_NAME, "span")
        for inner_text in text_elements:
            text.append(inner_text.get_attribute("innerText"))
        return text


    def _save_text(self, text_data: list):
        """
        Takes a list containing a dictionary of text data, and saves it in a file named after the friendly_ID
        in the raw_data directory
        
        Args:
            text_data: dictionary of the text data

        Raises:
            FileExistsError: an error occured when saving text that has already by saved. 
        """
        data_repo_path = os.path.abspath("raw_data")
        text_path = data_repo_path + "/" + text_data[0]["Friendly_ID"]  
        try:
            os.makedirs(text_path) #creates a file named the friendly ID in the Raw_Data directory
            with open(text_path + "/data.json", "w") as file:
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

    
    def _save_images(self, text_data: list, rsc_list: list):
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
   
   
    # def _upload_images_to_s3(self, file_name: str): #COMMENTED OUT FOR DOCKER IMAGE
    #     """
    #     Takes in a file name, and if the user wants to scrape images and upload them to S3,
    #     it uploads the image to S3. By default uses the friendly id generated in _extract_text().
        
    #     Args: 
    #         file_name: the name of the file you want to upload to S3
    #     """
    #     if scraper_variables.scrape_images and scraper_variables.upload:
    #          s3_client = boto3.client('s3')
    #          image_response = s3_client.upload_file(f'raw_data/{file_name}/images/{file_name}.jpeg', scraper_variables.bucket, file_name + ".jpeg")


    # def _add_to_df_batch (self, extracted_text: list): #COMMENTED OUT FOR DOCKER IMAGE
    #     """
    # Takes a list of dictionaries as input, converts the list of dictionaries into 
    # a pandas dataframe, then appends the dataframe to a the list of dataframes df_batch. 

    # Args:
    #     extracted_text: a list of dictionaries, each dictionary is a row in the dataframe
    #     """
    #     if scraper_variables.upload:
    #         df= pd.DataFrame(extracted_text)
    #         self.df_batch.append (df)


    # def _upload_batch_to_rds(self): #COMMENTED OUT FOR DOCKER IMAGE
    #     """
    # Checks if df_batch has reached the batch size specified in scraper_variables. If so, concatinates 
    # the list into a singe dataframe and uploads the dateframe to the RDS (also specified in scraper_variables)    
    #     """
    #     if scraper_variables.upload: #make these if gates cleaner
    #         if len (self.df_batch) == scraper_variables.batch_size:
    #             complete_df = pd.concat (self.df_batch) 
    #             complete_df = complete_df.astype ("str")
    #             engine = create_engine (scraper_variables.connenction_string) 
    #             complete_df.to_sql(scraper_variables.table_name, engine, if_exists='append') 
    #             self.df_batch = []


if __name__ == "__main__":
    my_scraper = Scraper()
    my_scraper.scrape()

