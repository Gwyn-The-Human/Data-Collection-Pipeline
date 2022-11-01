## Data-Collection-Pipeline

# A Quick and Fun Note on Ethics


# Rationale 
I tried scraping tiktok initially but all the interesting data needed a login, and tiktok blocks logins from the selenium-controlled browser - pretty effectivly I found out after some research. I left that for a later project and am using this oppertunity to gain the fluency I will need to explore more.
I'm really interested in popular narratives as a way of understanding a particular zeitgeist, ("what does the rise of Marvel movies imply about mainstream ways of thinking about ourselves and the world"), and I thought it would be cool to see an overview of the release and reception of different genres of film over time. Then as I worked on it I decided to try to generalise the scraper for use on other sites aswell.  


# The Scraper
I've imported selenium and chrome driver (since I'm using chrome as my browser), and using webdriver manager to keep the driver path consistent for other users. Also using urllib and beautifulsoup for image scraping, and uuid for generating id's for each insatance of data. 

On itialisation the scraper opens the 'browse by genre' page of imdb (used argpares to add an optional headless mode flag -hdls), saves the links to each genre. It will loop through each page and collects on release date, genre, rating, and number of ratings. 

File Guide
scraper: the main directory
    -scraper_main.py is the main project, a general data scraper
    -scraper_variables.py suppliments scraper.py; it's where you can add your own xpaths and customise the scraper for use on another site, and turn on or off image scraping. Right now those variables are set for scraping imdb. 

raw_data: where scraped data is stored. Text will be saved to ```raw_data/(friendly ID)/ data.json``` and images to ```raw_data/(friendly ID)/images/(friendly ID).jpeg```. If there is no raw_data directory, one will be created by default. 

scraper_test: directory holding tests:
    -test_methods is the main file containing some basic tests to see if the scraper is running correctly. 

Dockerfile: Used for playing around with building a docker image from the scraper. 

env.yaml: details about the conda environment I'm using

README.md: That's me! 

requirements.txt: called in Dockerfile to install dependancies during the docker build. 


# Generalising the Scraper 
Generalising the scraper for use on other websites has really cleaned up the code and been a great excercise in getting learning more about the proccess! I've also kept most methods public or protected for tweaking if needed. 

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
ALSO ALSO NOTE! Currently there is no page method so this scraper will only scraper the first page of every genre (thats still 2200 records!). BUT it would be really easy to add a next page method and add it wherever required in the scrape method loops. 


# Building Tests 
Developed a tests package using unnittest module, and added it to my python path. Given that the methods are built to be run with different inputs, the tests are for general features like checking that the lengths of the outputs corrolate correctly to the kinds of inputs. 


# Scalabaly Storing the Data
You can specify a Amazon Web Services RDS for storing tabular data remotly, as well as an S3 bucket for sotring images, although currently the scraper can only scraper text AND images or just text (not just images). 
Scraper_main.py use boto to upload images to an S3 bucket specified in scraper_variables, and uses sqlalchemy and pandas to generate a dataframe from the text data as the scraper runs, and then upload it to RDS when the frame has reached a specified size (saved as batch_size in scraper_variables). I decided to upload in batches for a few reasons: 

1-I want the scraper be able to save remotley without having to also save data locally, so I didn't want it to just iterate throught the locally saved data.json files. 
2 -If I upload it all at once, then you have to wait until the scraper has totally exhausted the webiste, and if it closed prematurely then it doesnt upload anything. 

So in batches you can customise how frequently during the scrape the data is uploaded, and so it avoids the above problems and isnt as slow and costly as uploading the data one record at a time. Pretty cool right?! 


# The Docker Container
This part has mostly just been practice with using docker for two reasons: 
    1- the functionality of the container is reduced (had to comment out uploading options since the container won't run with os.environ[myenvironmentvariables]) so it can only scrape locally and only run in headless mode. 
    2-had to use the --no sanbox tag in getting it to work which is aparently unsupported, but I'm not going to fix because of the first point ^^ 


# Features to be implemented 
    #a search bar method (e.g for searching something on linkedin)
    #login method 
    #an accept cookies method

