from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

#driver.get("https://www.amazon.in/")
#event_times = driver.find_element(By.CSS_SELECTOR, "event-widget time")
driver.get("https://en.wikipedia.org/wiki/Main_Page")
wiki_page = driver.find_element(By.XPATH, '//*[@id="articlecount"]/ul/li[2]/a[1]')
print(wiki_page.text)