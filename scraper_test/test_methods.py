
from scraper import scraper_main
from scraper import scraper_variables
from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
import json
import os
import pandas as pd
import shutil
import unittest




class ScraperTestCase (unittest.TestCase):
    
    def setUp(self):
        self.test_instance = scraper_main.Scraper()
        self.test_lib = [{"Friendly_ID":"TEST_FOLDER"}]
        self.maxDiff = None
        self.engine = create_engine (scraper_variables.connenction_string)


    def test_get_links(self): #make sure expected links are up to date before using!!
        test_url = "https://www.imdb.com/feature/genre/?ref_=nv_ch_gr"
        parent_xpath = '//*[@id="main"]/div[6]/span/div/div/div/div' 
        child_xpath = './/div[@class="table-row"]'
        test_links = self.test_instance.get_links (test_url, parent_xpath, child_xpath)
        expected_first_link = "https://www.imdb.com/search/title?genres=action&title_type=feature&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=facfbd0c-6f3d-4c05-9348-22eebd58852e&pf_rd_r=4XV143XPJ1YNAFGVQ00V&pf_rd_s=center-6&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvpop_1"
        expected_last_link = "https://www.imdb.com/search/title?genres=western&title_type=feature&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=facfbd0c-6f3d-4c05-9348-22eebd58852e&pf_rd_r=3DCAVS8WGKANS79VV64R&pf_rd_s=center-6&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_mvpop_24"
        self.assertEqual (test_links[0][0:90], expected_first_link[0:90]) # just checks first 90 charactes of URL because there are small variations past that point
        self.assertEqual (test_links[-1][0:90], expected_last_link[0:90])
        

    def test_extract_text(self): # make sure this test's last line is up to date with scraper_variables.data_catagories
        test_extracted_text = self.test_instance._extract_text("https://www.imdb.com/title/tt0091326/?ref_=vp_close")
        self.assertEqual(len(test_extracted_text[0]), len(scraper_variables.data_catagories)+2) #extract creates catagories as specified in scraper_variables.data_catagories, and adds two new catagories (friendly Id and UUID)
        catagories = []
        for catagory in test_extracted_text[0]: 
            catagories.append(catagory)
        self.assertEqual (catagories, ['Title', 'Year', 'Number_of_Ratings', 'Rating', 'Genre', 'Friendly_ID', 'UUID'])


    def test_save_data_text(self):
        self.test_instance._save_text (self.test_lib)
        with open ("raw_data/TEST_FOLDER/data.json", "r") as text:
            self.assertEqual(text.read(), json.dumps(self.test_lib))


    def test_save_images(self):
        scraper_variables.scrape_images = True
        self.test_instance.driver.get("https://www.imdb.com/title/tt0091326/?ref_=vp_close")
        self.test_instance._save_images(self.test_lib, self.test_instance._extract_images_rsc())
        self.assertEqual (str(os.listdir("raw_data/TEST_FOLDER/images")), "['TEST_FOLDER.jpeg']")
        shutil.rmtree("raw_data/TEST_FOLDER")


    def test_upload_batch_to_rds (self):
        scraper_variables.upload = True
        scraper_variables.batch_size = 3
        scraper_variables.table_name = "test_table"
        test_df = pd.DataFrame (self.test_lib)
        self.test_instance.df_batch = [test_df, test_df, test_df]
        self.test_instance._upload_batch_to_rds()
        expected_result = [(0, 'TEST_FOLDER'), (0, 'TEST_FOLDER'), (0, 'TEST_FOLDER')]
        self.assertEqual (self.engine.execute("SELECT * FROM test_table").fetchall(), expected_result)
        self.engine.execute ("DROP TABLE test_table")
