import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


class Parser:

    def __init__(self):
        url = "https://cleanny.by/"
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install(), )
        browser.get(url)
        self.soup = BeautifulSoup(browser.page_source, 'html.parser')
        browser.close()

    def get_standart_clean_info(self):
        standart_clean = self.soup.find(class_="standartClean")
        clean_zones = standart_clean.find("nav").find_all("p")
        for i in range(len(clean_zones)):
            clean_zones[i] = clean_zones[i].get_text()

        clean_zones_descriptions_html = standart_clean.find(class_="komnata").find(class_="container").find_all(
            class_="inside")
        clean_zones_descr = []
        for i in clean_zones_descriptions_html:
            bufer = []
            description_elements = i.find_all("li")
            for j in description_elements:
                text = j.get_text()
                bufer.append(text.replace('\n', '').replace("                                ", ' ').strip())

            clean_zones_descr.append(bufer)

        return clean_zones, clean_zones_descr

    def get_cleaner_info(self):
        cleaners_blocks_html = self.soup.find(class_="cleaners").find(class_="blocks")
        cleaners_array = []
        names = cleaners_blocks_html.find_all(class_="name")
        imgs = cleaners_blocks_html.find_all("img")
        experiences = cleaners_blocks_html.find_all(class_="name")
        descriptions = cleaners_blocks_html.find_all(class_="text")
        for i in range(len(names)):
            name = names[i].find("span").get_text().replace('/n', '').strip()
            img = imgs[i]["src"]
            self.download_cleaner_photo(name, img)
            experience = experiences[i].get_text().replace('/n', '').strip()
            description = descriptions[i].get_text().replace('/n', '').strip()
            cleaners_array.append([name, img, experience, description])

    def download_cleaner_photo(self, name, url):
        img_url = f"https://cleanny.by{url}"
        img_data = requests.get(img_url).content
        holder_path = os.path.abspath(__file__).rpartition("\\")[0]
        cleaner_img_path = holder_path + f"\\Images\\{name}.jpg"
        with open(cleaner_img_path, "wb") as img:
            img.write(img_data)