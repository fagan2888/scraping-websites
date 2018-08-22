from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import requests
import time
from tqdm import tqdm


class Film(object):
    def __init__(self):
        self.rank = ''
        self.name = ''
        self.link = ''
        self.year = ''
        self.poster_link = ''
        

def get_film_list():
    driver = webdriver.Remote(
        command_executor='http://172.17.0.2:4444/wd/hub', 
        desired_capabilities=DesiredCapabilities.CHROME
    )

    # get the html
    url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find('table', class_='chart full-width')
    
    filmList = []
    for td in table.find_all('td', class_='titleColumn'):
        fullTitle = td.text.strip().replace('\n', '').replace('      ', '')

        rank = int(fullTitle.split('.')[0])
        name = fullTitle.split('.')[1].split('(')[0]
        year = int(fullTitle.split('(')[1][:-1])
        link = 'https://www.imdb.com' + td.find('a')['href']

        newFilm = Film()
        newFilm.rank = rank
        newFilm.name = name
        newFilm.year = year
        newFilm.link = link
        
        filmList.append(newFilm)
    driver.quit()
    return filmList


def download_all_posters(filmList, path=None):
    driver = webdriver.Remote(
        command_executor='http://172.17.0.2:4444/wd/hub', 
        desired_capabilities=DesiredCapabilities.CHROME
    )
    
    if path is not None:
        if ~os.path.isdir(path):
            os.mkdir(path)
        os.chdir(path)
    
    for film in tqdm(filmList):
        driver.get(film.link)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        div = soup.find('div', class_='poster')
        imgLink = 'https://www.imdb.com' + div.find('a')['href']
        film.poster_link = imgLink
        
        driver.get(imgLink)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        div = soup.find_all('div', class_='pswp__zoom-wrap')
        img = div[1].find('img', class_='pswp__img')['src']
        
        f = open('{0}.jpg'.format(film.name.replace(':', '').encode('utf8').decode('utf8')), 'wb')
        f.write(requests.get(img).content)
        f.close()
        
        time.sleep(3)
        
    driver.quit()
    
    
        