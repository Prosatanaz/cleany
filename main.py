from pprint import pprint

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

url = "https://cleanny.by/"
options = Options()
options.headless = True
browser = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install(), )
browser.get(url)
soup = BeautifulSoup(browser.page_source, 'html.parser')
browser.close()
###поиск клинеров
cleaners = soup.find('div', 'cleaners')
cleaners_names_and_expirience = cleaners.find_all('p', 'name')

for cleaner_name_and_expirience in cleaners_names_and_expirience:
    print(cleaner_name_and_expirience.text)

descriptions =  cleaners.find_all('p','text')
for description in descriptions:
    print(description.text)

standart =  soup.find('div', 'mobileStandartClean')

room = standart.find('div', 'komnata').find('div','inside')
print(room.text)  
bathroom = standart.find('div', 'sanuzel').find('div','inside')
print(bathroom.text)
kitchen = standart.find('div', 'kuhnya').find('div','inside')
print(kitchen.text)
koridor = standart.find('div','koridor').find('div','inside')
print(koridor.text)


#print(soup.text)




