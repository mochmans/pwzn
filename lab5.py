import requests
from bs4 import BeautifulSoup
import json
import argparse

url = 'https://www.scrapethissite.com/pages/'

parser = argparse.ArgumentParser(description='Static scraper')
parser.add_argument('-f', '--filename', help='Filename to process (json)', default = 'pages')

args = parser.parse_args()

if args.filename[:-4] != 'json':
    filename = args.filename + '.json'
else:
    filename = args.filename

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

main_div = soup.find('div', class_ = 'col-md-6 col-md-offset-3')

page_list = main_div.find_all('div', class_='page')

pages = {}

for page in page_list:
    title = page.find('h3').text.strip()
    print(f'Title: {title}')
    description = page.find('p').text.strip()
    print(f'Description: {description}')

    pages[title] = description

    print('--------------------------------------')

with open('./' + filename, 'w') as f:
   json.dump(pages, f, indent=4)