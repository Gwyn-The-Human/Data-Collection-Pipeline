from setuptools import setup
from setuptools import find_packages

setup(
    name='Scraper', ## This will be the name your package will be published with
    version='0.0.1', 
    description='Customisable data scraper',
    url='https://github.com/Gwyn-The-Human/Data-Collection-Pipeline',                                                            
    author='Gwyn-The-Human', # Your name
    license='MIT',
    packages=find_packages(), # See notebook for detailed explanation
    install_requires=['requests', 'beautifulsoup4'], # For this project we are using two external libraries
                                                     # Make sure to include all external libraries in this argument
)