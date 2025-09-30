from bs4 import BeautifulSoup
import requests
import csv

URLS = [

    "https://www.geeksforgeeks.org/python/implementing-web-scraping-python-beautiful-soup/",

    "https://www.audible.com/search?keywords=book&node=18573211011",

]

filename_geeks = "geeksforgeeks_data.csv"
all_text_geeks = ""
da_response = requests.get(URLS[0])

da_soup = BeautifulSoup(da_response.content, "html.parser")

da_text_list = da_soup.find_all(name="p")

for da_p in da_text_list:
    all_text_geeks += da_p.getText()


all_links = []

da_anchor_list = da_soup.find_all(name="a")

for da_a in da_anchor_list:

    da_link = da_a.get("href")

    if da_link[0] != "#":
        all_links.append(da_link)
geeks_data = [
    ["Text", "Links"],
    [all_text_geeks, all_links],
]
with open(filename_geeks, "w", newline="") as da_geeks_file:

    da_writer = csv.writer(da_geeks_file, delimiter="|")

    da_writer.writerows(geeks_data)

filename_amazon = "amazon_imgs.csv"

all_imgs_links = []

da_response = requests.get(URLS[1])

da_soup = BeautifulSoup(da_response.content, "html.parser")

all_imgs = da_soup.find_all(name="img")

for da_img in all_imgs:

    all_imgs_links.append(da_img.get("src"))
data_amazon = [

    ["Links"],

    [all_imgs_links],

]

with open(filename_amazon, "w", newline="") as da_amazon_file:

    da_writer = csv.writer(da_amazon_file, delimiter="|")

    da_writer.writerows(data_amazon)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

ALL_URLS = [

    "https://www.amazon.com/",

]


da_options = webdriver.ChromeOptions()

da_options.add_experimental_option("detach", True)

da_webdriver = webdriver.Chrome(options=da_options) # Creating a webdriver object.

da_webdriver.get(ALL_URLS[0])

cont_button = WebDriverWait(da_webdriver, 20).until(ec.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div[3]/div/div/form/div/div/span/span/button")))

cont_button.click()
da_search = "Tails The Fox Plushie"
da_entry = WebDriverWait(da_webdriver, 30).until(ec.presence_of_element_located((By.XPATH, '//*[@id="twotabsearchtextbox"]')))

da_entry.send_keys(da_search)
da_entry.send_keys(Keys.ENTER)
da_correct_item = WebDriverWait(da_webdriver, 30).until(ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[4]/div/div/span/div/div/div[3]/div[1]/a')))
da_correct_item.click()