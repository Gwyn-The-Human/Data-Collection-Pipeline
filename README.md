# Data-Collection-Pipeline

Before using anything in this repo please read this quick and fun note on ethics: 

## Ethical Use Guide

### Why its important: 
1.These are real [lives at stake](https://fortune.com/2022/04/30/algorithm-screens-for-child-neglect-raises-concerns/)  
2.You don’t want to look [really really bad.](https://www.nytimes.com/2021/01/15/world/europe/dutch-government-resignation-rutte-netherlands.html%20)  

3.You don’t want to break the law and suffer [crippling EUR20mil fines.](https://gdpr-info.eu/issues/fines-penalties/#:~:text=83(4)%20GDPR%20sets%20forth,to%20that%20used%20in%20Art.)

### A brief guide on ethical use of the scraper
Here are a few things you can think about to make it less likely that you’ll run into the above issues, summarised for you from [ForHumanity's algorithm ethics course](https://forhumanity.center/forhumanity-university/), but please remember this guide is NOT at all exhaustive:

**1.**Set a clear objective. There’s no point in taking on unneccesary risks for data you don’t need. Be clear on what you actually need, and then only scrape that. 

**2.**Once you’ve set your objective, consider as many stakeholders as you can. Some might be: 
a)ME! This is my code! 
b)Users of whatever your building
c)Their immediate family and friends
d)You / your organisation
e)The environment! Think of the trees! 
f)The subjects of the data you are scraping.
g)You’re really smart, you can think of more. 

**3.**Go through each of your stakeholders and get creative about possible ways your choices could be harmful to them / benifetting them unequally. For this scraper that might include your choice of: 
    i)project (is it really something you want to do? etc.)
    ii)website to scrape (whose data are you scraping & have they consented? etc.)
    iii)data catagories (do you need this data? Could this data be misused? is it a protected catogery? Could it be used to infer protected catagories? etc.) 
    iv)data catagory labelling (is anything implied by how you label? Any associations unintended associations? etc.)
Ideally get a diverse group of people to discuss it with! Is there a little voice in your head that has a little bit of doubt? Great, You have found an instance of ethical choice! 

**4.**Say out loud : “I am encountering an instance of Ethical Choice.” Really say it, it will actually help. 

**5.**Take some time to research your issue to get a better understanding of how the mechanisms your choice can effect the relevant stakeholders.

**6.**Can you think of any ways to mitigate or avoid this issues in how you make the above choices? If so great, do that!!

**7.**Write down severity (0 is disturbance, 10 is death) vs. likelyhood (impossible, rare, unlikley, likely, certain) of forseeable consequences for each choice you’ll have to make, and decide what sort of risks you are willing to accept at which likelyhood. 

**8.**Check in with your gut about your descisions. If you had to tell your mother / your grandmother / your child / your environmentalist friend about your your choices, what do you think they would say. 

**9.**Lastly, remember that there are no right answers here! This guide is to help you keep yourself accountable to your own morals, not mine. If you have got to this point and are confident in your choice, go for it! 

**10.**Check in again in future to make sure you are still confident with your choices, given the things you’ve thought about so far, because things can change.

OK that’s it! Please remember that this guide is not exhaustive; for more info see the course here https://forhumanity.center/forhumanity-university/  (its free!) or reach out to me directly for resources or questions. I also would also love to hear about your experience using the guide, if you thought it was helpful and accesible etc. 

Thanks for taking the time! 


## Project Rationale 
I first and foremost am using this project to gain the fluency I will need to explore more data collection and later ML. 
I'm really interested in popular narratives as a way of understanding a particular zeitgeist, ("what does the rise of Marvel movies imply about mainstream ways of thinking about ourselves and the world"), and I thought it would be cool to see an overview of the release and reception of different genres of film over time. Then as I worked on it I decided to try to generalise the scraper for use on other sites aswell.  


## The Scraper
I've imported selenium and chrome driver (since I'm using chrome as my browser), and using webdriver manager to keep the driver path consistent for other users. Also using urllib and beautifulsoup for image scraping, and uuid for generating id's for each insatance of data. ## environment  environment 

On itialisation the scraper opens the 'browse by genre' page of imdb (used argpares to add an optional headless mode flag -hdls), saves the links to each genre. It will loop through each page and collects on release date, genre, rating, and number of ratings. 

File Guide
scraper: the main directory
    -scraper_main.py is the main project, a general data scraper
    -scraper_variables.py suppliments scraper.py; it's where you can add your own xpaths and customise the scraper for use on another site, an# environment d turn on or off image scraping. Right now those variables are set for scraping imdb. 

raw_data: where scraped data is stored. Text will be saved to ```raw_data/(friendly ID)/ data.json``` and images to ```raw_data/(friendly ID)/images/(friendly ID).jpeg```. If there is no raw_data directory, one will be created by default. 

scraper_test: directory holding tests:
    -test_methods is the main file containing some basic tests to see if the scraper is running correctly. 

Dockerfile: Used for playing around with building a docker image from the scraper. 

env.yaml: details about the conda environment I'm using

README.md: That's me! 

requirements.txt: called in Dockerfile to install dependancies during the docker build. 


## Generalising the Scraper 
Generalising the scraper for use on other websites has really cleaned up the code and been a great excercise in getting learning more about the proccess! I've also kept most methods public or protected for tweaking if needed. 

scraper_variables is where a user can customise the scraper for use on other websites. the get_links method can be called as many times as needed to get links to links to links to links...etc until you reach the pages you're trying to get to; in this instance, I am using it twice, calling the variables I use for it just parent/child_xpath_one and parent/childxpath_two for the first and second use# environment s respectivly.

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


## Building Tests 
Developed a tests package using unnittest module, and added it to my python path. Given that the methods are built to be run with different inputs, the tests are for the main methods, but not the overarching scrape method. 


## Scalabaly Storing the Data
You can specify a Amazon Web Services RDS for storing tabular data remotly, as well as an S3 bucket for sotring images, although currently the scraper can only scraper text AND images or just text (not just images). 
Scraper_main.py use boto to upload images to an S3 bucket specified in scraper_variables, and uses sqlalchemy and pandas to generate a dataframe from the text data as the scraper runs, and then upload it to RDS when the frame has reached a specified size (saved as batch_size in scraper_variables). I decided to upload in batches for a few reasons: 

1-I want the scraper be able to save remotly without having to also save data locally, so I didn't want it to just iterate throught the locally saved data.json files. 
2 -If I upload it all at once, then you have to wait until the scraper has totally exhausted the webiste, and if it closed prematurely then it doesnt upload anything. 

So in batches you can customise how frequently during the scrape the data is uploaded, and so it avoids the above problems and isnt as slow and costly as uploading the data one record at a time. Pretty cool right?! 


## The Docker Container
This part has mostly just been practice with using docker for two reasons: 
    1- the functionality of the container is reduced (had to comment out uploading options since the container won't run with os.environ [myenvironmentvariables]  so it can only scrape locally and only run in headless mode. 
    2-had to use the --no sanbox tag in getting it to work which is aparently unsupported, but I'm not going to fix because of the first point ^^ 

## workflow with Github Actions

The current workflow will update the "newscraper" on my dockerhub, but note that this is JUST FOR TESTING! i wanted to keep all the functions in the code in this repo (not lose functionlaity, see above) so the newscraper doesn't actually run. But it was a cool experience and a really powerful feature to have gained experience with! 

## Features to be implemented to scraper_main.py
    search bar method (e.g for searching something on linkedin)
    login method 
    accept cookies method

