from setuptools import setup
from setuptools import find_packages

setup(
    name='Scraper', ## This will be the name your package will be published with
    version='0.0.1', 
    description='Customisable data scraper',
    url='https://github.com/Gwyn-The-Human/Data-Collection-Pipeline',                                                            
    author='Gwyn-The-Human', # Your name
    license='MIT',
    packages=find_packages(),
    install_requires=[
'argparse',
'boto3',
'bs4',
'packaging',
'pandas', 
'scraper', 
'selenium', 
'sqlalchemy', 
'urllib3',
'uuid',
'webdriver_manager',
], 
)