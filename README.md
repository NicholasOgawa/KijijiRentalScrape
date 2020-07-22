# KijijiRentalScrape

Scraping housing data from Kijiji and storing it into an MySQL table. Allows for refinable house features. For example, if you are only looking for a 1-bedroom apartment or a furnished basement, just put in the link to the first page of whatever specifications you have created via Kijiji and the table will only pull links which meet the requirement.

## Prerequisites

Dependencies: selenium, requests, bs4, re, MySQL

```bash

pip install requests bs4 regex selenium
```


Install [ChomeDriver](https://chromedriver.storage.googleapis.com/index.html?path=84.0.4147.30/)

###  MySQL installation
1. Install [MySQL](https://dev.mysql.com/downloads/mysql/)

 
2. via CLI: Accessing as a root user  & Write in the password below
```bash
$ mysql -u root -p
Enter password: 
```
ii) If everything goes accordingly, this is what to to expect
```bash
Welcome to the MySQL monitor.  Commands end with ;
...
mysql> 
```
iii) Create & Use database:
```
mysql> CREATE DATABASE kijijidb;
mysql> USE kijijidb;
```

iv) After running the KijijiScraper, run query
```bash
mysql> select * from VancouverRentals;
```


## Usage 


```python
import KijijiScraper
 
Scraper = KijijiScraper.Scrape('https://www.kijiji.ca/b-apartments-condos/vancouver/1+bedroom/c37l1700287a27949001', host= 'localhost', user= 'root',
password = 'password', database = 'kijijidb', table = 'VancouverRentals')

Scraper.createtable() #Execute only once for each KijijiScraper Object, in this example a table named VancouverRentals will be created

Scraper.StartScrape() #Takes link and will add all current houses to SQL table. 

```

## Future Improvements

- Remove BeautifulSoup and Request dependencies since it is only used for 1 method.

- Pandas Dataframe cleaning and analysis.




