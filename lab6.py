from asyncio import wait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import argparse
import json

parser = argparse.ArgumentParser(description='Dynamic scraper')
parser.add_argument('-f', '--filename', help='Filename to process (json)', default = 'overview')

args = parser.parse_args()

if args.filename[:-4] != 'json':
    filename = args.filename + '.json'
else:
    filename = args.filename




url = "https://www.wowhead.com"


options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)

service = webdriver.FirefoxService()

driver.get(url)

button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[id="onetrust-accept-btn-handler"]'))
)
button.click()

driver.switch_to.default_content()


time.sleep(2)

link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.header-wrapper > div.header > div.header-nav-wrapper > div.header-nav-features > a.header-nav-text.header-nav-classes')))
link.click()

element = driver.find_element(
    By.CSS_SELECTOR,
    "a[href*='warlock/destruction/overview-pve-dps']"
)

driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    element
)

link2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#warlock > div.class-info.hub-info > ul:nth-child(6) > li:nth-child(3) > a')))
link2.click()


element = driver.find_element(
    By.CSS_SELECTOR,
    "#overview"
)
text = driver.execute_script("""
const overview = document.querySelector('#overview');
let result = '';

for (let node of overview.nextSibling.parentNode.childNodes) {
    if (node.nodeType === Node.TEXT_NODE) {
        result += node.textContent;
    }
    if (node.nodeType === Node.ELEMENT_NODE && node.tagName === 'BR') {
        result += ' ';
    }
}
return result.trim();
""")



with open('./' + filename, 'w') as f:
   json.dump(text, f, indent=4)

print(text)

time.sleep(5000)