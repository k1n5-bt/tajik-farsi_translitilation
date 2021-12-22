import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

EXE_PATH = r'C:\Users\K1n5\Desktop\nlp\parser_url\chromedriver.exe'  # EXE_PATH это путь до ранее загруженного нами файла chromedriver.exe

caps = DesiredCapabilities.CHROME
caps["pageLoadStrategy"] = "none"

ua = dict(DesiredCapabilities.CHROME)
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x935')
lastDate = '2011-08-13'

driver = webdriver.Chrome(desired_capabilities=caps, executable_path=EXE_PATH, chrome_options=options)
driver.get(
    f'https://twitter.com/search?q=(from%3ABBCTajikistan)%20until%3A{lastDate}%20since%3A2010-02-13-filter%3Areplies&src=typed_query&f=live')
count = 0
links = set()
time.sleep(10)
SCROLL_PAUSE_TIME = 5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    if count >= 3000:
        count = 0
        driver.quit()
        driver = webdriver.Chrome(desired_capabilities=caps, executable_path=EXE_PATH, chrome_options=options)
        driver.get(
    		f'https://twitter.com/search?q=(from%3ABBCTajikistan)%20until%3A{lastDate}%20since%3A2010-02-13-filter%3Areplies&src=typed_query&f=live')
        time.sleep(5)
        last_height = driver.execute_script("return document.body.scrollHeight")
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(5)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    date = driver.find_element_by_tag_name('time')
    lastDate = date.get_attribute("datetime")[0:10]
    sbtn = driver.find_elements_by_tag_name('span')
    for i in sbtn:
        if 'bbc.in' in i.text:
            links.add(i.text[-20:])
        elif 'bit.ly' in i.text:
            links.add(i.text[-20:])
        count += 1
    print(f'OK - Links count: {len(links)} Date: {lastDate}')
    driver.delete_all_cookies()
print(*links)
result = ''
for i in links:
    result += f'{i}\n'
with open('result1.txt', 'w', encoding="utf-8") as w:
    w.write(result)