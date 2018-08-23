from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import requests
import time
from tqdm import tqdm

class Room(object):
    def __init__(self):
        title = ''
        district = ''
        price = ''
        rank = ''
        review = ''
        guests = ''
        room_type = ''
        beds = ''
        baths = ''
        items = ''
 

def get_room_list(org_url):
    driver = webdriver.Remote(
        command_executor='http://172.17.0.2:4444/wd/hub', 
        desired_capabilities=DesiredCapabilities.CHROME
    )
    
    roomList = []
    
    for i in tqdm(range(17)):
        if i!=0:
            url = org_url + '&section_offset=' + str(i)
        else:
            url = org_url
        
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        roomTable = soup.find('div', class_='_fhph4u')
        
        for room in roomTable.find_all('div', '_gig1e7'):
            new_room = Room()

            detail_info = room.find_all('div', class_='_1nhodd4u')

            new_room.title = room.find(itemprop='name')['content'].split(' - ')[0]
            new_room.district = room.find(itemprop='name')['content'].split(' - undefined - ')[1]
            new_room.price = int(float(
                room.find('span', '_pd52isb').text.split('$')[1].split(' TWD')[0].replace(',', '')
            ))

            new_room.guests = int(float(detail_info[0].text.split('、')[0].replace('位', '')))
            new_room.room_type = detail_info[0].text.split('、')[1]
            new_room.beds = int(float(detail_info[0].text.split('、')[2].split('張')[0]))
            new_room.baths = int(float(detail_info[0].text.split('、')[3].split('間')[0]))
            new_room.items = detail_info[1].text.split(' · ')

            rank, review = None, None
            if '評價' in room.text:
                try:
                    rank = float(room.find('span', class_='_q27mtmr').find('span', role='img')['aria-label'].split('評分是')[1].split('（')[0])
                    review = int(float(room.find('span', class_='_1gvnvab').text))
                except:
                    print(i, new_room.title)
            new_room.rank = rank
            new_room.review = review

            roomList.append(new_room)
    return roomList