url = 'https://www.imdb.com/feature/genre/?ref_=nv_ch_gr'

#scrape text or text and images?

scrape_text = True
scrape_images = False


#layers, used in get_links() method

parent_xpath_one = '//*[@id="main"]/div[6]/span/div/div/div/div' 
child_xpath_one = './/div[@class="table-row"]'

parent_xpath_two = '//*[@id="main"]/div/div[3]/div'
child_xpath_two = './/div[@class="lister-item mode-advanced"]'


# data catagories (text), used in extract_text() method (if fewer than two, you'll need a new method for generating friendly ID)

data_catagory_one_tag="Title"
data_catagory_one_XPATH='/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1'

data_catagory_two_tag="Year"
data_catagory_two_XPATH='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[1]/a'

data_catagory_three_tag="Number of Ratings"
data_catagory_three_XPATH='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/div/div/div[2]/div[3]'

data_catagory_four_tag ="Rating"
data_catagory_four_XPATH='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]'

data_catagory_five_tag = "Genre"
data_catagory_five_XPATH = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]'

#image attributes used in extract_image
image_attributes = {'class' : 'ipc-image', "loading": "eager" , "sizes": "50vw, (min-width: 480px) 34vw, (min-width: 600px) 26vw, (min-width: 1024px) 16vw, (min-width: 1280px) 16vw"}


#so right now it looks like:
#for x in get_links (layer one):
    #for y in get links (layer two):
        #get text
        #save text
        #get image
        #save imag 
        #CAN I MAKE THE SAVE FUNCITON WORK FOR BOTH? 

