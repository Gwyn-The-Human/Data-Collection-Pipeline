url = 'https://www.imdb.com/feature/genre/?ref_=nv_ch_gr'


#scrape text and/or images? (if you only want to scrape images it is still reccomended to 
#scrape two catagories text data as well to generate friendly IDs, otherwise IDs will be random)

scrape_text = True
scrape_images = True


 
#layers, used in get_links() method. Different layers are for using get_links() on differently structured pages. 

parent_xpath_one = '//*[@id="main"]/div[6]/span/div/div/div/div' 
child_xpath_one = './/div[@class="table-row"]'

parent_xpath_two = '//*[@id="main"]/div/div[3]/div'
child_xpath_two = './/div[@class="lister-item mode-advanced"]'

layers_dict = {parent_xpath_one:child_xpath_one, parent_xpath_two:child_xpath_two} #used in test_units to iterate to test get_links() for different layers



# text data catagories used in extract_text() method in the format { tag : XPATH} 
# ( can add or remove as needed,if fewer than two, you'll need to edit extract_text () for generating friendly ID)

data_catagories = { 

    'Title' : '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1',

    'Year' : '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[1]/a',

    'Number of Ratings' : '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/div/div/div[2]/div[3]',

    'Rating' : '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]',

    'Genre' : '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]',

}



#image attributes used in extract_image()

image_attributes = {'class' : 'ipc-image', "loading": "eager" , "sizes": "50vw, (min-width: 480px) 34vw, (min-width: 600px) 26vw, (min-width: 1024px) 16vw, (min-width: 1280px) 16vw"}


#IN PROGRESS : 

#number of pages you want the scraper to scrape, used in next_page().  

number_of_nexts = 3

#'next' button location used in next_page()
next_button_XPATH = '//*[@id="main"]/div/div[1]/div[2]/a[2]'
