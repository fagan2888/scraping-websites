from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from bs4 import BeautifulSoup
import requests
import time
from tqdm import tqdm


htmlInfo = [
    {'name': 'span', 'class_': 'player-summary__player-number'},
    {'name': 'p', 'class_': 'player-summary__first-name'},
    {'name': 'p', 'class_': 'player-summary__last-name'},
    {'name': 'span', 'class_': 'player-summary__team-name'},
    {'name': 'div', 'string': 'PTS'},
    {'name': 'div', 'string': 'REB'},
    {'name': 'div', 'string': 'AST'},
    {'name': 'div', 'string': 'PIE'},
    {'name': 'div', 'string': 'HT'},
    {'name': 'div', 'string': 'WT'},
    {'name': 'div', 'string': 'AGE'},
    {'name': 'div', 'string': 'BORN'},
    {'name': 'div', 'string': 'PRIOR'},
    {'name': 'div', 'string': 'DRAFT'},
    {'name': 'div', 'string': 'EXP'},
]



class Player(object):
    def __init__(self):
        self.first_name = ''
        self.last_name = ''
        self.link = ''
        self.player_number = ''
        self.team_name = ''
        self.PTS = ''
        self.REB = ''
        self.AST = ''
        self.PIE = ''
        self.HT = ''
        self.WT = ''
        self.AGE = ''
        self.BORN = ''
        self.PRIOR = ''
        self.DRAFT = ''
        self.EXP = ''


def get_player_list():
    driver = webdriver.Remote(
        command_executor='http://172.17.0.2:4444/wd/hub', 
        desired_capabilities=DesiredCapabilities.CHROME
    )

    # get the html
    url = 'http://stats.nba.com/players/list/'
    driver.get(url)

    # get the table of players
    soup = BeautifulSoup(driver.page_source, 'lxml')
    div = soup.find('div', class_='columns / small-12 / section-view-overlay')

    # get all the players' links
    playerList = []
    for player in div.find_all('li', class_='players-list__name'):
        new_player = Player()
        new_player.link = player.find('a')['href']
        new_player.name = player.text
        playerList.append(new_player)
    return playerList

def get_player_details(playerList, image=False, path=None):
    driver = webdriver.Remote(
            command_executor='http://172.17.0.2:4444/wd/hub', 
            desired_capabilities=DesiredCapabilities.CHROME
    )
    
    if path is not None:
        if ~os.path.isdir(path):
            os.mkdir(path)
        os.chdir(path)
    
    for p in tqdm(playerList):
        time.sleep(3)
        
        # get the html
        driver.get('http://stats.nba.com' + p.link)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        for info in htmlInfo:
            if 'string' in info.keys():
                key = info['string']
                value = soup.find(**info).findNextSibling()

            else:
                key = info['class_'].split('player-summary__')[1].replace('-', '_')
                value = soup.find(**info)
            
            try:
                setattr(p, key, value.text)
            except:
                setattr(p, key, None)
            
                
        if image:
            div = soup.find('div', class_='player-summary__image-block')
            img = div.find('img')['src']

            try:
                img_name = '{0} {1}.jpg'.format(p.first_name, p.last_name)
            except:
                img_name = '{0}.jpg'.format(p.name)

            try: 
                f = open(img_name, 'wb')
                f.write(requests.get(img).content)
            except:
                print(p.name)
            f.close()
            
    return playerList

def get_player_image(playerList, path=None):
    driver = webdriver.Remote(
        command_executor='http://172.17.0.2:4444/wd/hub', 
        desired_capabilities=DesiredCapabilities.CHROME
    )
    if path is not None:
        if ~os.path.isdir(path):
            os.mkdir(path)
        os.chdir(path)
    
    for p in tqdm(playerList):
        
        url = 'http://stats.nba.com' + p.link
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        div = soup.find('div', class_='player-summary__image-block')
        img = div.find('img')['src']
        
        try:
            img_name = '{0} {1}.jpg'.format(p.first_name, p.last_name)
        except:
            img_name = '{0}.jpg'.format(p.name)
        
        f = open(img_name, 'wb')
        f.write(requests.get(img).content)
        f.close()
        
        time.sleep(3)