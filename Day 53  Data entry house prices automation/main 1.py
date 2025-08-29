from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.common.devtools.v136.css import CSSRule

header = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=2,3&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Nagpur&BudgetMin=80-Lacs")
time.sleep(5)

all_property_cards = driver.find_elements(by=By.CSS_SELECTOR, value="div.mb-srp__card")
prices_list = []
descriptions_list = []
for card in all_property_cards:
    price_element = card.find_elements(by=By.CSS_SELECTOR, value="div.mb-srp__card__price--amount")
    description_element = card.find_elements(by=By.CSS_SELECTOR, value="p.two-line-truncated")

    if description_element:
        descriptions_list.append(description_element[0].text)

    if price_element:
        prices_list.append(price_element[0].text)

print(prices_list)
print(descriptions_list)

for n in range(len(prices_list)):
    # TODO: Add fill in the link to your own Google From
    driver.get("https://forms.gle/ufG8VXbLGNWTLK1u8")
    time.sleep(2)

    # Use the xpath to select the "short answer" fields in your Google Form.
    # Note, your xpath might be different if you created a different form.
    address = driver.find_element(by=By.XPATH,
                                  value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(by=By.XPATH,
                                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH,
                               value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(by=By.XPATH,
                                        value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address.send_keys(descriptions_list[n])
    price.send_keys(prices_list[n])
    submit_button.click()