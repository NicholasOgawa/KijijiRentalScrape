from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import re
import logging
import mysql.connector

driver = webdriver.Chrome()

class KijijiListings():
    
    def __init__(self, url):
        self.url = url 
        self.listings = []
        self.allUrls = []
    
    def get_listings(self, url, pages):
        link = re.findall(r'(?:[^/]|//)+', url)
        baseurl = link[0]
        urlprefix , urlsuffix = '/'.join(link[:-1]) , link[-1]
        page_no = 1
        # This will be in __init__ 
    
        for i in range(pages): #Retrieving individual pages 
            target_page = f"{urlprefix}/page-{page_no}/{urlsuffix}"
            r = requests.get(target_page)
            soup = BeautifulSoup(r.content, "html5lib")
            listingdivs = soup.select('a[class*=title]')
            page_no += 1
    
            for i in range(len(listingdivs)): #Retrieving all the links from each kijiji listing page    
                propsuffix = listingdivs[i]['href']
                requestpt2 = (f"{baseurl}{propsuffix}")
                self.listings.append(requestpt2)
    
    def indhousedata(self):
        for link in self.listings:
            driver.get(link)
            id_ = link[-10:]
            titleList = driver.find_elements_by_class_name('title-2323565163')
            
            try:
                date_time = driver.find_element_by_tag_name('time').get_attribute("datetime")
                date = re.match(r'[^A-Z]*', date_time).group(0)
                
            except NoSuchElementException:
                date = None
                
                if not titleList[0].text:
                    title = titleList[1].text

            else:
                title = titleList[0].text
    
            addlen = driver.find_elements_by_class_name('address-3617944557')
    
            if len(addlen) is 1:
                address = driver.find_elements_by_class_name('address-3617944557')[0].text.replace(',','').strip()
            else:
                address = driver.find_elements_by_class_name('address-3617944557')[1].text.replace(',','').strip()
    
            data = driver.find_element_by_id('vip-body').text.replace('\n',' ').replace('$','Price ')
    
            replacechar = ['(',')', ',', ':']
    
            for character in replacechar:
                data = data.replace(character,'')
     
            data = data.split('View Map Posted') # This obscure line here is for 1 reason, since we are using Regex to scrape the data. We need to ensure the Regex does not retrieve information from the title

            try:
                price = re.search(r'Price (\d+)', data[0]).group(1)      
    
            except AttributeError:
                price = None
    
            utilities = re.search(r'(\S+) Utilities Included', data[0]).group(1)
        
            type_ = re.search(r'(\S+) Bedrooms ', data[1]).group(1)
    

            bedrooms = re.search(r' Bedrooms (\S+)', data[1]).group(1)
            if bedrooms == 'Bachelor/Studio':
                bedrooms = 0
    
            bathrooms = re.search(r' Bathrooms (\d+)', data[1]).group(1)
            furnished =  re.search(r'Furnished (\S+)', data[1]).group(1)
            outdoor = re.search(r'Personal Outdoor Space (\S+)', data[1]).group(1)
            pets = re.search(r' Pet Friendly (\S+)', data[1]).group(1)    
            utilities = re.search(r'(\S+) Utilities Included', data[0]).group(1)

            try:
                sqft = re.search(r' The Unit Size sqft (\d+)', data[1]).group(1)
            except AttributeError:
                sqft = None
        
            self.allUrls.append([ id_ ,title, date, price, address, bathrooms, bedrooms, sqft, furnished, outdoor, pets,
                                  utilities,type_, link])

class SQLInitializaion():
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = mysql.connector.connect(host=self.host,
                                       user=self.user,
                                       password=self.password,
                                       database = self.database)
    
        logging.info(f'Initalized MySQL')

class KijijiScraper(KijijiListings):
    def __init__(self, url, host, user, password, database, tablename):
        super().__init__(url)
        self.SQLconnection = SQLInitializaion(host,user,password,database)
        self.tablename = tablename
        
    def createtable(self): 
        cursor = self.SQLconnection.conn.cursor()
        creation = f"""
                CREATE TABLE {self.tablename} 
                (id int PRIMARY KEY, title varchar(80),
                date date, price int,
                address varchar(80),bathrooms int,
                bedrooms int, sqft int,
                furnished varchar(10), outdoor varchar(20),
                pets varchar(10), utilities varchar(10),
                type varchar(25), url varchar(150) UNIQUE)"""
        
        cursor.execute(creation)
        self.SQLconnection.conn.close()
        
    def listToSQL(self):
        conn = self.SQLconnection.conn
        cursor = self.SQLconnection.conn.cursor()
        logging.info(f'Inserting rows into {self.tablename}')
        
        stmt = f"""
          INSERT INTO {self.tablename} 
          (id, title, date, price,
          address, bathrooms, bedrooms, sqft,
          furnished, outdoor, pets, utilities,
          type, url) 
          VALUES (%s, %s, %s, %s, %s, %s, %s,
          %s, %s, %s, %s, %s, %s, %s) 
          ON DUPLICATE KEY UPDATE id = id
          """
        
        cursor.executemany(stmt, self.allUrls)
        conn.commit()
        conn.close()
    
    def StartScrape(self):
        self.get_listings(self.url, 1)
        self.indhousedata()
        self.listToSQL()
    
    def ConvertToPandas(self):
        conn = self.SQLconnection.conn
        cursor = self.SQLconnection.conn.cursor()
        cursor.execute(f"SELECT * FROM {self.tablename}")
        rows = cursor.fetchall()
        df = pd.DataFrame(table_rows, columns = [ 'id' ,'title', 'date', 'price', 'address'
                                       , 'bathrooms', 'bedrooms', 'sqft', 'furnished', 'outdoor', 'pets',
                                       'utilities', 'type', 'url'])
        conn.close()
        
        return df
        
if __name__ = '__main__':
    scraper = KijijiScraper(url = 'https://www.kijiji.ca/b-apartments-condos/vancouver/1+bedroom/c37l1700287a27949001',
                           host = "localhost", user = "root", password = '', database = 'db',
                            tablename= 'rental')
    scraper.StartScrape()
