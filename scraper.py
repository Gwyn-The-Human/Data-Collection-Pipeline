
#TODO make image scrape method
#TODO do i want to be saying page or url? maybe page is nicer


from socket import inet_ntoa
from selenium import webdriver
from selenium.webdriver.common.by import By
import uuid
import os
import scraper_variables
from bs4 import BeautifulSoup
import requests
import urllib.request


class scraper ():


    def __init__(self):
        self.path = "/home/gwyn/miniconda3/condabin/chromedriver" 
        self.driver = webdriver.Chrome (self.path) 
        if os.path.exists ("raw_data") == False:
            os.makedirs ("raw_data")
        

    def scrape (self): 
        layer_one_links = self.get_links(scraper_variables.url, scraper_variables.parent_xpath_one, scraper_variables.child_xpath_one)#lists links to genres 
        for link in layer_one_links: #for each genre link 
            layer_two_links = self.get_links (link, scraper_variables.parent_xpath_two, scraper_variables.child_xpath_two) #lists links to pages to be scraped
            for link in layer_two_links:#for each page link
                text_data = self.extract_text(link)
                rsc_list = self.extract_images_rsc # will return None if scraper_variables.scrape_text == False
                self.save_data (text_data, rsc_list) 


    def get_links(self, url, parent_xpath, child_xpath): 
        """
        Returns list of links within child elements of the given parent.
        If the child element has multiple links, this function returns the first link. 
        """
        links =[]
        self.driver.get (url)
        parent = self.driver.find_element (By.XPATH, parent_xpath)
        children = parent.find_elements (By.XPATH, child_xpath)
        for element in children:
            a_tag = element.find_element(By.TAG_NAME, 'a') 
            link= a_tag.get_attribute ('href')
            links.append(link)
        return links
   

    def extract_text (self, link):#do i need to specify a url here? 
        self.driver.get (link)
        data_catagory_one =  self.driver.find_element(By.XPATH, value=scraper_variables.data_catagory_one_XPATH).get_attribute('innerText') 
        data_catagory_two = self.driver.find_element(By.XPATH, value=scraper_variables.data_catagory_two_XPATH).get_attribute('innerText') 
        data_catagory_three = self.driver.find_element(By.XPATH, value= scraper_variables.data_catagory_three_XPATH).get_attribute('innerText') 
        data_catagory_four = self.driver.find_element (By.XPATH, scraper_variables.data_catagory_four_XPATH).get_attribute('innerText')
        data_catagory_five = self.get_multiple_elements_text (scraper_variables.data_catagory_five_XPATH) 
   
        compiled_data = {

            scraper_variables.data_catagory_one_tag : data_catagory_one,
            scraper_variables.data_catagory_two_tag : data_catagory_two,
            scraper_variables.data_catagory_three_tag : data_catagory_three,
            scraper_variables.data_catagory_four_tag : data_catagory_four,
            scraper_variables.data_catagory_five_tag : data_catagory_five,

            'Friendly ID' : f"{data_catagory_one}-{data_catagory_two}", #maybe need to add one more detail to this ID
            'UUID': str(uuid.uuid4())
            }

        return compiled_data


    def get_multiple_elements_text(self, xpath): 
        """
        For instances where one instance of text data is located accross multiple elements under a single parent element. 
        """
        text = []
        parent = self.driver.find_element(By.XPATH, xpath)
        text_elements = parent.find_elements (By.TAG_NAME, "span")
        for inner_text in text_elements:
            text.append (inner_text.get_attribute('innerText'))
        return text


    def save_text(self, text_data):#image data optional but text required
        data_repo_path = os.path.abspath("raw_data")
        text_path = data_repo_path + "/" + text_data ["Friendly ID"]   
        try:
            os.makedirs(text_path) #made a file named the friendly ID in the Raw_Data directory
            with open(text_path+ "/data.json" , "w") as file:
                file.write (str(text_data))
        except FileExistsError:
            print (f"file {text_data['Friendly ID']} already saved!")


    def extract_images_rsc (self, image_attributes):
        if scraper_variables.scrape_images == False:
            return None
        rsc_list = []
        html_page = requests.get('https://www.imdb.com/title/tt10648342/?ref_=adv_li_tt')
        soup = BeautifulSoup(html_page.content, 'html.parser')
        pics = soup.find_all("img", attrs = image_attributes) 
        for pic in pics: #the for statement loops through pics (a list) and allows for more tahn one image to be scraped. 
            rsc_list.append (pic ["src"])
        return rsc_list


    def save_images (self, text_data, rsc_list):#uses text_data to get file's friendly ID
        if scraper_variables.scrape_images == False:
            return None
        image_path = f"raw_data/{text_data['Friendly ID']}/images"
        if os.path.exists (image_path) == False:
            os.makedirs (image_path)
        for pic_rsc in rsc_list:
            urllib.request.urlretrieve (pic_rsc, f"{image_path}/{text_data['Friendly ID']}.jpeg"),  


    def scroll_to_bottom (self):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    

    def next_page (self):
        next_button_cell= driver.find_element(By.CLASS_NAME, value= "desc")
        a_tag = next_button_cell.find_element(By.TAG_NAME, value= 'a')
        next_link = a_tag.get_attribute ('href')
        self.driver.get (next_link)
        # TODO add a while loop so it will stop scrolling once it hits the final next. 



if __name__ == "__main__":
    my_scraper = scraper()
    
    text_data = my_scraper.extract_text ('https://www.imdb.com/title/tt10648342/?ref_=adv_li_tt')
    rsc_list = my_scraper.extract_images_rsc (scraper_variables.image_attributes)
    my_scraper.save_text (text_data)
    my_scraper.save_images (text_data, rsc_list)
    