import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://scholar.google.co.uk/citations?hl=en&user=mfZtyl4AAAAJ&view_op=list_works&sortby=title'
# parsing only the first 20 titles of this page
# output to Excel with Title, Cited by, year

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.323',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
FILE = 'ANYNAME.csv' #file name
def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr', class_='gsc_a_tr')
    articles = []
    for item in items:
        articles.append({
            'title': item.find('a', class_='gsc_a_at').get_text(),
            'cited by': item.find('td', class_='gsc_a_c').get_text(),
            'year': item.find('td', class_='gsc_a_y').get_text()
        })
    return articles

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'cited by', 'year'])
        for item in items:
            writer.writerow([item['title'], item['cited by'], item['year']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        articles = []
        for page in range(1, 2):
            html = get_html(URL, params={'page': page})
            articles.extend(get_content(html.text))
        save_file(articles, FILE) #
        print(articles)
    else:
        print("Error")


parse()

#created by Ayarini