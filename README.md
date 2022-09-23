# Data-Collection-Pipeline


# Rationale 
I tried scraping tiktok initially but all the interesting data needed a login, and tiktok blocks logins from the selenium-controlled browser - pretty effectivly I found out after some research. I left that for a later project and am using this oppertunity to gain the fluency I will need to explore more.
I'm really interested in popular narratives as a way of understanding a particular zeitgeist, ("what does the rise of Marvel movies imply about mainstream ways of thinking about ourselves and the world"), and I thought it would be cool to see an overview of the release and reception of different genres of film over time. Then as I worked on it I decided to try to generalise the scraper for use on other sites aswell.  

# The Scraper
I've imported selenium and chrome driver (since I'm using chrome as my browser). Also using urllib and beautifulsoup for image scraping, and uuid for generating id's for each insatance of data. 
On itialisation the scraper opens the 'browse by genre' page of imdb, saves the links to each genre. It will loop through each page and collects on release date, genre, rating, and number of ratings. 

File Guide
scraper: the main directory
    -scraper_main.py is the main project, a general data scraper
    -scraper_variables.py suppliments scraper.py; it's where you can add your own xpaths and customise the scraper for use on another site, and turn on or off image scraping. Right now those variables are set for scraping imdb. 

raw_data: where scraped data is stored. Text will be saved to ```raw_data/(friendly ID)/ data.json``` and images to ```raw_data/(friendly ID)/images/(friendly ID).jpeg```. If there is no raw_data directory, one will be created by default. 

scraper_test: directory holding tests:11
    -test_methods is the main file containing some basic tests to see if the scraper is running correctly. 

# Generalising the Scraper 

Generalising the scraper for use on other websites has really cleaned up the code and been a great excercise in getting learning more about the proccess! I've also kept most methods public for tweaking if needed. 

scraper_variables is where a user can customise the scraper for use on other websites. the get_links method can be called as many times as needed to get links to links to links to links...etc until you reach the pages you're trying to get to; in this instance, I am using it twice, calling the variables I use for it just parent/child_xpath_one and parent/childxpath_two for the first and second uses respectivly.

NOTE! get_links will ONLY return links from the children of the FIRST element it finds at the given parent_xpath!
    If you are looking for anything other than the first element at the given parent_xpath, you can change the index below:
    ```
            children = parent[0].find_elements (By.XPATH, child_xpath)
    ```
ALSO NOTE! get_links will ONLY return the first link it finds in a child element.  
    If you are looking for anything other than the first link of the child element, you can change the index below:
    ```
            link= a_tag[0].get_attribute ('href')
    ``` 

# Building Tests 

    Developed a tests package using unnittest module, and added it to my python path. Given that the methods are built to be run with different inputs, the tests are for general features like checking that the lengths of the outputs corrolate correctly to the kinds of inputs. 


# Features to be implemented


# environment 