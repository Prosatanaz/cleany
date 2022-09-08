import os
from os import path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import httplib2
import gspread

class Parser:

    def __init__(self):
        url = "https://cleanny.by/"
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install(), )
        browser.get(url)
        self.soup = BeautifulSoup(browser.page_source, 'html.parser')
        browser.close()
        holder_path = os.path.abspath(__file__).rpartition("\\")[0]
        gc = gspread.service_account(f"{holder_path}\clinny-361618-f313b3437739.json")
        worksheet = gc.open_by_url(
            "https://docs.google.com/spreadsheets/d/115gY9pcQghGnjV5FLfnDZELuTu6invP72rK40sb3em8/edit#gid=0")
        holder_path = os.path.abspath(__file__).rpartition("\\")[0]

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

        self.set_standart_clean_info_gsheet(clean_zones, clean_zones_descr)

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
            img_path = f"Cleaners_photo\\{name}.jpg"
            experience = experiences[i].get_text().replace('/n', '').strip()
            description = descriptions[i].get_text().replace('/n', '').strip()
            cleaners_array.append([name, img_path, experience, description])

        self.set_cleaners_info_gs(cleaners_array)

    @classmethod
    def download_cleaner_photo(self, name, url):
        if not os.path.exists(f"{self.holder_path}\\Cleaners_photo"):
            os.mkdir(f"{self.holder_path}\\Cleaners_photo")

        img_url = f"https://cleanny.by{url}"
        h = httplib2.Http('.cache')
        response, content = h.request(img_url)
        cleaner_img_path = self.holder_path + f"\\Cleaners_photo\\{name}.jpg"
        out = open(cleaner_img_path, "wb")
        out.write(content)
        out.close()

    def collect_reviews(self):
        if not os.path.exists(f"{holder_path}\\reviews"):
            os.mkdir(f"{self.holder_path}\\reviews")

        reviews_html = self.soup.find(class_="reviewsCarousel owl-carousel owl-loaded owl-drag").find_all(class_="owl-item")
        reviews = []
        for i in range(len(reviews_html)):
            review = reviews_html[i].find(class_="item")
            review_url = review.find("img")["src"]
            img_url = f"https://cleanny.by{review_url}"
            h = httplib2.Http('.cache')
            response, content = h.request(img_url)
            review_img_path = self.holder_path + f"\\reviews\\{review_url.replace('/', '')}"
            out = open(review_img_path, "wb")
            out.write(content)
            out.close()
            reviews.append(review_img_path)

        self.set_reviews_gs(reviews)

    @classmethod
    def set_standart_clean_info_gsheet(self, clean_zones, clean_zones_description):
        clean_sheet = self.worksheet.get_worksheet(1)
        clean_sheet.clear()
        for i in range(len(clean_zones)):
            clean_sheet.append_row([clean_zones[i], "\n".join(clean_zones_description[i])])

    @classmethod
    def set_cleaners_info_gs(self, cleaners):
        cleaners_sheet = self.worksheet.get_worksheet(0)
        cleaners_sheet.clear()
        cleaners_sheet.append_row(["Имя", "Фото", "Стаж", "Описание"])
        for i in cleaners:
            cleaners_sheet.append_row(i)

    @classmethod
    def set_reviews_gs(self, reviews):
        reviews_sheet = self.worksheet.get_worksheet(2)
        reviews_sheet.clear()
        reviews_sheet.append_row(["Отзывы"])
        for i in reviews:
            reviews_sheet.append_row([i])