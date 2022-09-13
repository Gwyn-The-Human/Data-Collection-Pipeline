# Data-Collection-Pipeline


# The Target: I.M.D.B 
I tried scraping tiktok initially but all the interesting data needed a login, and tiktok blocks logins from the selenium-controlled browser - pretty effectivly I found out after some research. I left that for a later project and am using this oppertunity to gain the fluency I will need to explore more.
I'm really interested in popular narratives as a way of understanding a particular zeitgeist, ("what does the rise of Marvel movies imply about mainstream ways of thinking about ourselves and the world"), and I thought it would be cool to see an overview of the release and reception of different genres of film over time. 

# The Scraper
I've imported selenium and chrome driver (since I'm using chrome as my browser). On itialisation the scraper opens the 'browse by genre' page of imdb, saves the links to each genre. It will loop through each page and collect data on release date, genre, rating, and number of ratings, although I havn't implimented this part yet! 

File Guide
-scraper.py is the main project, a general data scraper
-scraper_variables.py suppliments scraper.py; it's where you can add your own xpaths and customise the scraper for use on another site, and turn on or off image scraping. Right now those variables are set for scraping imdb. 

-imdb_scraper.py is the first draft; a scraper hard-coded for imdb.
-tiktok_scraper.py is the beggining of the discontinued tiktok scraper.
-zupla_test.py and testo.py are both spaces for testing selenium and XPATH calls.



# Generalising the Scraper 

Generalising the scraper for use on other websites has really cleaned up the code and been a great excercise in getting learning more about the proccess! 

scraper_variables is where a user can customise the scraper for use on other websites. the get_links method can be called as many times as needed to get links to links to links to links...etc until you reach the pages you're trying to get to; in this instance, I am using it twice, calling the variables I use for it just parent/child_xpath_one and parent/childxpath_two for the first and second use respectivly.

The get links is similar to the get_multiple_elements_text, which also searches for and returns multiple elements, but I thought it would be simpler to not try to get that functionality into one method and instead kept them seperate. 

Similarily I worked out a method to save text and optionally images as well, but I think its a lot more readable to have two seperate methods for saving images and saving text so thats what I went with. 