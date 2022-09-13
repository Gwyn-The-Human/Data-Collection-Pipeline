
#TODO make image scrape method


from socket import inet_ntoa
from selenium import webdriver
from selenium.webdriver.common.by import By
import uuid
import os
import scraper_variables



class scraper ():


    def __init__(self):
        self.path = "/home/gwyn/miniconda3/condabin/chromedriver" 
        self.driver = webdriver.Chrome (self.path) 
        if os.path.exists ("raw_data") == False:
            os.makedirs ("raw_data")
        

    def get_links(self, url, parent_xpath, child_xpath): 
        """
        Returns list of links within child elements of the given xpath.
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
   


    def scrape (self): 
        layer_one_links = self.get_links(scraper_variables.url, scraper_variables.parent_xpath_one, scraper_variables.child_xpath_one)#lists links to genres 
        print (f"genres are {layer_one_links}")
        for link in layer_one_links: #for each genre link 
            pages = self.get_links (link, scraper_variables.parent_xpath_two, scraper_variables.child_xpath_two) #lists links to pages to be scraped
            for page in pages:
                self.save_data (self.extract_text(page))
                


    def save_data(self, data):
            data_repo_path = os.path.abspath("raw_data")
            product_path = data_repo_path + "/" + data ["Friendly ID"]   
            try:
                os.makedirs(product_path) #made a file named the friendly ID in the Raw_Data directory
                with open(product_path+ "/data.json" , "w") as file:
                    file.write (str(data))
            except FileExistsError:
                print ("file already saved!")

            #self.extract_image (film)


    def extract_text (self, page):
        
        self.driver.get (page) #just for testing
        
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
        For instances where one catagory of text data is located accross multiple elements under a single parent element. 
        """
        text = []
        parent = self.driver.find_element(By.XPATH, xpath)
        text_elements = parent.find_elements (By.TAG_NAME, "span")
        for inner_text in text_elements:
            text.append (inner_text.get_attribute('innerText'))
        return text


    def extract_image (self, film):
        pass


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
    print(my_scraper.compile_text('https://www.imdb.com/title/tt10648342/?ref_=adv_li_tt'))
    my_scraper.save_data(my_scraper.compile_text ('https://www.imdb.com/title/tt10648342/?ref_=adv_li_tt'))