FROM python:3.9 

RUN apt-get update && apt-get install -y gnupg2 \
    && wget --no-check-certificate -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get -y update \
#installs chrome 
    && apt-get install -y google-chrome-stable \
#downloads chrome driver
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
#unzips
    && apt-get install -yqq unzip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ 
COPY . .

RUN pip install -r requirements.txt
#runs the scraper
CMD [ "python", "data-collection-pipeline/scraper_main.py" ]