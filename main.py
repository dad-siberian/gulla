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

from parse_tululu_category import parse_category


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


def download_image(url, folder='images'):
    os.makedirs(folder, exist_ok=True)
    basename = os.path.basename(url)
    if basename == 'nopic.gif':
        filename = basename
    else:
        filename = f'{basename}'
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


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_page', nargs='?', default=1, type=int)
    parser.add_argument('end_page', nargs='?', default=5, type=int)
    return parser


def get_book_id(url):
    book_id = urlparse(url).path
    return ''.join(item for item in book_id if item.isdecimal())


def main():
    logging.basicConfig(
        filename='sample.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )
    log = logging.getLogger('ex')
    parser = create_parser()
    namespace = parser.parse_args()
    
    book_urls = parse_category(namespace.start_page, namespace.end_page + 1)
    for book_url in tqdm(book_urls):
        book_id = get_book_id(book_url)
        while True:
            try:
                soup = get_soup(book_url)
                book_details = parse_book_details(soup, book_url)
                cover_url = book_details.get('img_url')
                book_title = book_details.get('title')
                download_txt(book_id, book_title)
                download_image(cover_url)
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
        with open("books.json", "a", encoding='utf8') as my_file:
            json.dump(book_details, my_file, ensure_ascii=False)


if __name__ == '__main__':
    main()
