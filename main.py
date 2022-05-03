import argparse
import logging
import os
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def download_txt(book_id, filename, folder='books'):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f'{book_id}. {filename}')
    url = f'http://tululu.org/txt.php'
    params = {'id': book_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    with open(f'{filepath}.txt', 'wb') as file:
        file.write(response.content)


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.HTTPError


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return BeautifulSoup(response.text, 'lxml')


def get_cover_url(soup, base_url):
    img_url = soup.find('div', class_='bookimage').find('img')['src']
    return urljoin(base_url, img_url)


def download_image(url, book_id, folder='images'):
    os.makedirs(folder, exist_ok=True)
    basename = os.path.basename(url)
    if basename == 'nopic.gif':
        filename = basename
    else:
        filename = f'{book_id}_{basename}'
    filepath = os.path.join(folder, filename)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def parse_book_page(soup):
    title_tag = soup.find('body').find('h1').text.split('::')
    genres = soup.find('span', class_='d_book').find_all('a')
    comments = soup.find_all('div', class_='texts')
    book_page = {
        'title': sanitize_filename(title_tag[0].strip()),
        'author': sanitize_filename(title_tag[1].strip()),
        'genre': [genre.text for genre in genres],
        'comments': [comment.find('span').text for comment in comments],
    }
    return book_page


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_id', nargs='?', default=1, type=int)
    parser.add_argument('end_id', nargs='?', default=10, type=int)
    return parser


def main():
    logging.basicConfig(
        filename='sample.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )
    log = logging.getLogger('ex')
    parser = createParser()
    namespace = parser.parse_args()
    for book_id in range(namespace.start_id, namespace.end_id + 1):
        base_url = f'https://tululu.org/b{book_id}'
        while True:
            try:
                soup = get_soup(base_url)
                cover_url = get_cover_url(soup, base_url)
                book_title = parse_book_page(soup)['title']
                download_txt(book_id, book_title)
                download_image(cover_url, book_id)
            except requests.HTTPError:
                log.exception(
                    f"redirect to the homepage. "
                    f"Maybe book number {book_id} isn't on the website."
                )
            except requests.exceptions.ConnectionError:
                time.sleep(30)
                continue
            break


if __name__ == '__main__':
    main()
