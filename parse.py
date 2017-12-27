import csv
from bs4 import BeautifulSoup
import requests

url = 'https://www3.lenovo.com/by/ru/laptops/c/Laptops'


def get_html(url):
    try:
        response = requests.get(url, timeout = 5)
        return response.content
    except requests.exceptions.ConnectTimeout:
        print('Oops. Connection timeout occured!')
    except requests.exceptions.ConnectionError:
        print('Oops. Connection error occured')
    except requests.exceptions.MissingSchema:
        print('Invalid URL')

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    names = []
    number=0
    for table in soup.find_all('div', class_ = 'model-title'):

        names.append({
            'title' : 'Lenovo '+table.text.strip(),
            'description' : [i.text.strip() for i in soup.find_all('div', class_ = 'model-descript')][number]
        })
        number+=1
    return names

def save(names, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Название', 'Описание'))

        for name in names:
            writer.writerow((name['title'], ''.join(name['description'])))

def main():
    save(parse(get_html(url)), 'notebooks.csv')

if __name__ == '__main__':
    main()
