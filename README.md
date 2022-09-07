# Data-Collection-Pipeline


# The Target: I.M.D.B 
I tried scraping tiktok initially but all the interesting data needed a login, and tiktok blocks logins from the selenium-controlled browser - pretty effectivly I found out after some research. I left that for a later project and am using this oppertunity to gain the fluency I will need to explore more.
I'm really interested in popular narratives as a way of understanding a particular zeitgeist, ("what does the rise of Marvel movies imply about mainstream ways of thinking about ourselves and the world"), and I thought it would be cool to see an overview of the release and reception of different genres of film over time. 

# The Scraper
I've imported selenium and chrome driver (since I'm using chrome as my browser). On itialisation the scraper opens the 'browse by genre' page of imdb, saves the links to each genre. It will loop through each page and collect data on release date, genre, rating, and number of ratings, although I havn't implimented this part yet! 
