import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium import webdriver

EXE_PATH = r'C:\Users\K1n5\Desktop\nlp\parser_url\msedgedriver.exe'  # EXE_PATH это путь до ранее загруженного нами файла chromedriver.exe


def delete_cache():
    driver.execute_script("window.open('');")
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    driver.get('chrome://settings/clearBrowserData')  # for old chromedriver versions use cleardriverData
    time.sleep(2)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3)  # send right combination
    actions.perform()
    time.sleep(2)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 4 + Keys.ENTER)  # confirm
    actions.perform()
    time.sleep(5)  # wait some time to finish
    driver.close()  # close this tab
    driver.switch_to.window(driver.window_handles[0])  # switch back


# caps = DesiredCapabilities.CHROME
# caps["pageLoadStrategy"] = "none"

# ua = dict(DesiredCapabilities.CHROME)
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x935')

driver = webdriver.Edge(executable_path=EXE_PATH)

driver.get(
    'https://twitter.com/search?q=(from%3Abbcpersian)until%3A2014-09-16%20since%3A2010-02-13%20-filter%3Areplies&src=typed_query&f=live')

links = set()
time.sleep(10)
SCROLL_PAUSE_TIME = 5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(5)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    sbtn = driver.find_elements_by_partial_link_text("bbc.in")
    for i in sbtn:
        links.add(i.text)
    print(f'OK - Links count: {len(links)}')
    driver.delete_all_cookies()

print(*links)
result = ''
for i in links:
    result += f'{i}\n'
with open('result.txt', 'w', encoding="utf-8") as w:
    w.write(result)
driver.save_screenshot('screen_test_twit.png')
