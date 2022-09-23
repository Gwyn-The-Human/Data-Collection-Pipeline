
from scraper import scraper_main
from scraper import scraper_variables
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import shutil
import unittest

class ScraperTestCase (unittest.TestCase):
    
    def setUp(self):
        self.path = "/home/gwyn/miniconda3/condabin/chromedriver" 
        self.driver = webdriver.Chrome (self.path)
        self.test_instance = scraper_main.Scraper()
        self.test_lib = {"Friendly ID":"TEST_FOLDER"}


    def test_get_links(self):
        self.driver.get(scraper_variables.url)
        links_number = len(self.test_instance.get_links (scraper_variables.url, scraper_variables.parent_xpath_one, scraper_variables.child_xpath_one))
        parent = self.driver.find_element(By.XPATH, scraper_variables.parent_xpath_one)
        children_number = len (parent.find_elements(By.XPATH, scraper_variables.child_xpath_one))
        print (children_number)
        self.assertEqual (links_number,children_number)


    def test_extract_text(self):
        output = self.test_instance.extract_text("https://www.imdb.com/title/tt0091326/?ref_=vp_close")
        self.assertEqual(len(output), len(scraper_variables.data_catagories)+2)


    def test_save_data_text(self):
        self.test_instance.save_text (self.test_lib)
        with open ("raw_data/TEST_FOLDER/data.json", "r") as text:
            self.assertEqual(text.read(), str(self.test_lib))


    def test_save_images(self):
        self.test_instance.save_images (self.test_lib, self.test_instance._extract_images_rsc("https://www.imdb.com/title/tt0091326/?ref_=vp_close"))
        self.assertEqual (str(os.listdir("raw_data/TEST_FOLDER/images")), "['TEST_FOLDER.jpeg']")
        shutil.rmtree("raw_data/TEST_FOLDER")


