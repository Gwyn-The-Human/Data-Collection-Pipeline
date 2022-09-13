from cgitb import text
from email.mime import image
from operator import contains
from selenium import webdriver
PATH = "/home/gwyn/miniconda3/condabin/chromedriver" 
driver =webdriver.Chrome (PATH) 
from selenium.webdriver.common.by import By
import uuid
import os
import scraper_variables
from bs4 import BeautifulSoup
import requests
import urllib.request



def extract_images_src (image_attributes):
    rsc_list = []
    html_page = requests.get('https://www.imdb.com/title/tt10648342/?ref_=adv_li_tt')
    soup = BeautifulSoup(html_page.content, 'html.parser')
    pics = soup.find_all("img", attrs = image_attributes) 
    for pic in pics: #the for statement loops through pics (a list) and allows for more tahn one image to be scraped. 
        rsc_list.append (pic ["src"])
    return rsc_list

def save_images (file_id,rsc_list):
    for pic_rsc in rsc_list:
        urllib.request.urlretrieve (pic_src, f"{file_id}.jpeg"), 


def save_both (*image_rsc_or_text_data): #needs to take text_data
    try:
        print (texty)
        try:
            print (imagey)
        except NameError:
            print ("no image given")
    except NameError:
        print ("no text given")
        try:
            print (imagey)
        except NameError:
            print ("method has received no data")

def fun (a,b):
    print ("ok")

fun ("a")