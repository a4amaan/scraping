import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from pdf2jpg import pdf2jpg
import os
from PyPDF2 import PdfMerger

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}


def merge():
    x = [a for a in os.listdir('pdf') if a.endswith(".pdf")]
    merger = PdfMerger()
    for pdf in x:
        merger.append(open(f'pdf/{pdf}', 'rb'))
    with open("result.pdf", "wb") as fout:
        merger.write(fout)


def worksheet(link, folder):
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        sheets = soup.findAll('a')
        for sheet in sheets:
            link = sheet['href']
            if str(link).endswith('.pdf'):
                print('downloading', link)
                r = requests.get(link, headers=headers)
                url = urlparse(link)
                filename = os.path.basename(url.path)
                filepath = f'{folder}/{filename}'
                outputpath = filename.replace(".pdf", "")
                # outputpath = f'img/{outputpath}.png'
                with open(filepath, 'wb') as f:
                    f.write(r.content)
                # result = pdf2jpg.convert_pdf2jpg(filepath, 'pdf')


def worksheets(link, folder):
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        sheets = soup.findAll('div', {'class': 'pin'})
        for sheet in sheets:
            s = sheet.findNext('a', {'class': 'PinImage'})
            sheet_link = s['href']
            if not os.path.exists(folder):
                os.makedirs(folder)
            worksheet(sheet_link, folder)
    else:
        print(response.status_code)


def categories():
    response = requests.get('https://www.worksheetfun.com/math/', headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        cats = soup.findAll('li', {'class': 'cat-item'})
        for cat in cats:
            link = cat.findNext('a')
            worksheets(link['href'], str(link.text).replace(' ', '-').strip())
    else:
        print(response.status_code)


if __name__ == '__main__':
    categories()
    # worksheets('https://www.worksheetfun.com/category/math-worksheetfunmenu/addition/addition-2-digit/')
    # worksheet('https://www.worksheetfun.com/2016/02/26/10-more-10-less-1-more-1-less-four-worksheets/')
    # merge()
