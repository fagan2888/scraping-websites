from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
from tqdm import tqdm

class Book(object):
    def __init__(self):
        self.link = ''
        self.book_name = ''
        self.description = ''
        self.isbn = ''
        

def get_book_list(url):
    driver = webdriver.Remote(
        command_executor='http://172.17.0.2:4444/wd/hub', 
        desired_capabilities=DesiredCapabilities.CHROME
    )
    
    bookList = []
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    for i in soup.find('div', {'id': 'resultsCol'}).find_all('li'):
        try: 
            link = i.find('a', class_='a-link-normal a-text-normal')['href']
            if 'https://www.amazon.com/' not in link:
                link = 'https://www.amazon.com' + link
            book = Book()
            book.link = link
            bookList.append(book)
        except:
            pass
    return bookList


def get_book_details(bookList):
    driver = webdriver.Remote(
        command_executor='http://172.17.0.2:4444/wd/hub', 
        desired_capabilities=DesiredCapabilities.CHROME
    )
    
    for book in tqdm(bookList):
        driver.get(book.link)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        book.book_name = soup.find('h1', {'id': 'title'}).findNext().text
        book.isbn = soup.find('div', class_='content').find_all('li')[3].text.replace('ISBN-10: ', '')
        
        # get book description
        driver.switch_to_frame(driver.find_element_by_id('bookDesc_iframe'))
        soup2 = BeautifulSoup(driver.page_source, 'lxml')
        description = ''
        for element in soup2.find_all('h4'):
            title = '-'*5 + element.text + '-'*5
            content = element.findNext().text
            description = description + title + '\n' + content + '\n\n'
        
        if description == '':
            for element in soup2.find('div', {'id': 'iframeContent'}).findChildren():
                description = description + element.text + '\n'
            
        book.description = description
        
        time.sleep(3)
    return bookList