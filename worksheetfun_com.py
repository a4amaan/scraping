import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}


def worksheet(link):
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        sheets = soup.findAll('a')
        for sheet in sheets:
            link = sheet['href']
            if str(link).endswith('.pdf'):
                r = requests.get(link, headers=headers)
                url = urlparse(link)
                filename = os.path.basename(url.path)
                with open(f'data/{filename}', 'wb') as f:
                    f.write(r.content)


def worksheets(link):
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        sheets = soup.findAll('div', {'class': 'pin'})
        for sheet in sheets:
            sheet_link = sheet.findNext('a', {'class': 'PinImage'})['href']
            print(sheet_link)
    else:
        print(response.status_code)


def categories():
    response = requests.get('https://www.worksheetfun.com/math/', headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        cats = soup.findAll('li', {'class': 'cat-item'})
        for cat in cats:
            link = cat.findNext('a')['href']
            print(link)
    else:
        print(response.status_code)


if __name__ == '__main__':
    # categories()
    # worksheets('https://www.worksheetfun.com/category/math-worksheetfunmenu/addition/addition-2-digit/')
    worksheet('https://www.worksheetfun.com/2016/02/26/10-more-10-less-1-more-1-less-four-worksheets/')
