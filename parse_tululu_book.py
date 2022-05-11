import argparse
import json
import logging
import os
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from tqdm import tqdm


def download_txt(book_id, filename, folder='books'):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f'{book_id}. {filename}')
    url = f'https://tululu.org/txt.php'
    params = {'id': book_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    with open(f'{filepath}.txt', 'wb') as file:
        file.write(response.content)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


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


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return BeautifulSoup(response.text, 'lxml')


def parse_book_details(soup, base_url):
    title_tag = soup.find('body').find('h1').text.split('::')
    title, author = title_tag
    genres = soup.find('span', class_='d_book').find_all('a')
    img_url = soup.find('div', class_='bookimage').find('img').get('src')
    comments = soup.find_all('div', class_='texts')
    book_details = {
        'title': sanitize_filename(title.strip()),
        'author': sanitize_filename(author.strip()),
        'genre': [genre.text for genre in genres],
        'comments': [comment.find('span').text for comment in comments],
        'img_url': urljoin(base_url, img_url),
    }
    return book_details


def get_book(book_url):
    book_id_patch = urlparse(book_url).path
    book_id =''.join(item for item in book_id_patch if item.isdecimal())
    soup = get_soup(book_url)
    book_details = parse_book_details(soup, book_url)
    cover_url = book_details.get('img_url')
    book_title = book_details.get('title')
    download_txt(book_id, book_title)
    download_image(cover_url, book_id)
    return book_details


def create_parser():
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
    parser = create_parser()
    namespace = parser.parse_args()
    books = []
    for book_id in tqdm(range(namespace.start_id, namespace.end_id + 1)):
        book_url = f'https://tululu.org/b{book_id}/'
        while True:
            try:
                book = get_book(book_url)
                books.append(book)
            except requests.HTTPError:
                log.exception(
                    f"An HTTP error occurred. "
                    f"Maybe book number {book_id} isn't on the website."
                )
            except requests.exceptions.ConnectionError:
                log.exception(f"A Connection error occurred")
                time.sleep(30)
                continue
            break
    with open('books.json', 'a') as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
