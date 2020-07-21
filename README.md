# KijijiRentalScrape

Scraping housing data from Kijiji and storing it into an MySQL table. Allows for refinable house features. For example, if you are only looking for a 1-bedroom apartment or a furnished basement, just put in the link to the first page of whatever specifications you have created via Kijiji and the table will only pull links which meet the requirement.

## Prerequisites

Dependencies: selenium, requests, bs4, re, MySQL

'''bash
pip install requests bs4 re selenium pandas
'''

Link to installing [ChomeDriver](https://chromedriver.storage.googleapis.com/index.html?path=84.0.4147.30/)

## Usage 

'''python
import KijijiScraper
 
Scraper = KijijiScraper.Scrape('https://www.kijiji.ca/b-apartments-condos/vancouver/1+bedroom/c37l1700287a27949001', host= 'localhost', user= 'root',
password = 'password', database = 'db', table = 'VancouverRentals')

Scraper.createtable() #Only done once

Scraper.StartScrape() #Takes link and will add all current houses to SQL table
'''



