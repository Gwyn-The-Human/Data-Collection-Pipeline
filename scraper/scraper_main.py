#could i make it a parent class and put all those variables in __init__? and then have a child class be imdb.scraper etc etc. 
#TODO possible added features: 
    #add a search bar method (e.g for searching something on linkedin)
    #add login method from tiktok_scraper.py 
#TODO (optional) make it remove that extra images file to make it more direct if its images only? 
#TODO update setup.py deets 

#TODO add path to scraper variables to make it customisable, or make it a parameter (?)
#TODO changes assert to self.assertTrue or whatever

#add try except in my functionality to address the issue of multiple xpaths?
#suggest some texts?  --> ok 
#public - methods the user can use without any problem;  protected-> _function; still accesible BUT you dont rly want it to be , and private; liteally not accesible. 


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests
from scraper import scraper_variables
import urllib.request
import uuid


class Scraper ():

    def __init__(self):
        self.path = "/home/gwyn/miniconda3/condabin/chromedriver" 
        self.driver = webdriver.Chrome (self.path) 
        if os.path.exists ("raw_data") == False:
            os.makedirs ("raw_data")


    def scrape (self):
        """
        The main method that combines the other methods. Should be customised for use on other websites. 

        """ 
        layer_one_links = self.get_links(scraper_variables.url, scraper_variables.parent_xpath_one, scraper_variables.child_xpath_one)#lists links to genres 
        for link in layer_one_links: #for each genre link 
            layer_two_links = self.get_links (link, scraper_variables.parent_xpath_two, scraper_variables.child_xpath_two) #lists links to pages to be scraped
            for link in layer_two_links:#for each page link
                extracted_text = self.extract_text (link)
                my_scraper.save_text (extracted_text)
                my_scraper.save_images (extracted_text, self._extract_images_rsc (link) )# will return None if scraper_variables.scrape_text == False


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
       
        links =[]
        self.driver.get (link) #DO I NEED THIS? i need someway to navigate to the given URLS at each layer; maybe the for loop works fine for that
        parent = self.driver.find_elements (By.XPATH, parent_xpath)
        children = parent[0].find_elements (By.XPATH, child_xpath)
        for element in children:
            a_tag = element.find_elements(By.TAG_NAME, 'a') 
            link= a_tag[0].get_attribute ('href')
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
            A dictionary of the data scraped from the page, and associated IDs.
    """
        if scraper_variables.scrape_text == False:
            return {"UUID": str(uuid.uuid4())}
        
        self.driver.get (link)
        compiled_data = {}
        for catagory in scraper_variables.data_catagories:
            compiled_data [catagory] = self.driver.find_element(By.XPATH, scraper_variables.data_catagories[catagory]).get_attribute ('innerText')
        return self.__add_ids(compiled_data)
        

    def __add_ids (self, compiled_data):
        compiled_data ["Friendly ID"] = compiled_data [list(compiled_data)[0]] + "-" + compiled_data [list(compiled_data)[1]] #uses list () to index the dictionary compiled_data
        compiled_data ["UUID"] = str(uuid.uuid4())
        return compiled_data


    def _get_multiple_elements_text(self, xpath): 
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
        text_elements = parent.find_elements (By.TAG_NAME, "span")
        for inner_text in text_elements:
            text.append (inner_text.get_attribute('innerText'))
        return text


    def save_text(self, text_data):
        """
        Takes a dictionary of text data, and saves it in a file named after the friendly ID
        in the raw_data directory
        
        Args:
            text_data: dictionary of the text data

        Raises:
            FileExistsError: an error occured when saving text that has already by saved. 
        """
        if scraper_variables.scrape_text == False:
            return None
        data_repo_path = os.path.abspath("raw_data")
        text_path = data_repo_path + "/" + text_data ["Friendly ID"]   
        try:
            os.makedirs(text_path) #made a file named the friendly ID in the Raw_Data directory
            with open(text_path+ "/data.json" , "w") as file:
                file.write (str(text_data))
        except FileExistsError:
            print (f"file {text_data['Friendly ID']} already saved!")


    def _extract_images_rsc (self, link):
        """
        Returns a list of image sources with attributes specified in scraper_variables.image_attributes
        from the given link. 
        
        Args:
            link: (str) a url of the page being scraped
        """
        if scraper_variables.scrape_images == False:
            return None
        rsc_list = []
        html_page = requests.get(link)
        soup = BeautifulSoup(html_page.content, 'html.parser')
        pics = soup.find_all("img", attrs = scraper_variables.image_attributes) 
        for pic in pics: #the for statement loops through pics (a list) and allows for more than one image to be scraped. 
            rsc_list.append (pic ["src"])
        return rsc_list

    
    def save_images (self, text_data, rsc_list):#could this be a static method? pros? cons? 
        # Still needs to access scraper_variables!! 
        """
        Takes a list of image rscs and downloads them to a folder named after the file's friendly ID
        
        Args:
            text_data: a dictionary containing the text data for the file
            rsc_list: a list of image rsc's
        """
        if scraper_variables.scrape_images == False:
            return None
        image_path = f"raw_data/{text_data['Friendly ID']}/images"
        if os.path.exists (image_path) == False:
            os.makedirs (image_path)
        for pic_rsc in rsc_list:
            urllib.request.urlretrieve (pic_rsc, f"{image_path}/{text_data['Friendly ID']}.jpeg"),  


    def next_page (self, button_XPATH): #HMMMMMMMM maybe this just needs to all go in scrape()! 
        counter = 0
        while counter < scraper_variables.number_of_nexts:
            try:
                self.driver.find_element(By.XPATH, button_XPATH).click()
                counter +=1
            except NoSuchElementException:
                print ("next button not found. Maybe no more pages left.")
                break


        next_button_cell= driver.find_element(By.XPATH, value= "desc")
        a_tag = next_button_cell.find_element(By.TAG_NAME, value= 'a')
        next_link = a_tag.get_attribute ('href')
        self.driver.get (next_link)
        # TODO add a while loop so it will stop scrolling once it hits the final next. 
        #TODO generlalise this! 
        #TODO is this just click
        extracted_text = self.extract_text (link)
        my_scraper.save_text (extracted_text)
        my_scraper.save_images (extracted_text, self._extract_images_rsc (link) )


if __name__ == "__main__":
    my_scraper = Scraper()
    
    #extracted =  my_scraper.extract_text("https://www.imdb.com/title/tt10648342/?ref_=adv_li_tt")
    #print (extracted)
    #my_scraper.save_text (extracted)
   #my_scraper.save_images(extracted, my_scraper.extract_images_rsc ("https://www.imdb.com/title/tt10648342/?ref_=adv_li_tt"))
