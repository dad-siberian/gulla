import argparse
import json
import logging
import os
import time
from pathlib import Path
from urllib.parse import urljoin

from requests import ConnectionError, HTTPError
from tqdm import tqdm

from parse_tululu_book import get_book, get_soup


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def parse_book_urls(soup):
    base_url = 'https://tululu.org/'
    book_urls = list()
    book_hyperlinks = soup.select('div.bookimage a')
    for link in book_hyperlinks:
        book_href = link.get('href')
        book_urls.append(urljoin(base_url, book_href))
    return book_urls


def create_books_json(books, namespace):
    if namespace.json_path:
        base_path = namespace.json_path
    elif namespace.dest_folder:
        base_path = namespace.dest_folder
    else:
        base_path = '.'
    os.makedirs(base_path, exist_ok=True)
    json_path = os.path.join(base_path, 'books.json')
    with open(json_path, 'a') as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page', nargs='?', type=int, required=True)
    parser.add_argument('--end_page', nargs='?', default=701, type=int)
    parser.add_argument('--dest_folder', nargs='?', type=Path)
    parser.add_argument('--skip_imgs', action='store_const', const=True)
    parser.add_argument('--skip_txt', action='store_const', const=True)
    parser.add_argument('--json_path', nargs='?', type=Path)
    return parser


def main():
    file_handler = logging.FileHandler('sample.log')
    formatter = logging.Formatter(
        '%(asctime)s %(filename)s %(name)s %(levelname)s %(message)s'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    parser = create_parser()
    namespace = parser.parse_args()
    books = list()
    print(namespace.json_path)
    for page_number in tqdm(range(namespace.start_page, namespace.end_page)):
        fiction_url = f'https://tululu.org/l55/{page_number}/'
        soup = get_soup(fiction_url)
        book_urls = parse_book_urls(soup)
        for book_url in tqdm(book_urls):
            while True:
                try:
                    book = get_book(
                        book_url,
                        namespace.dest_folder,
                        namespace.skip_imgs,
                        namespace.skip_txt,
                    )
                    books.append(book)
                except HTTPError:
                    logger.exception(f"An HTTP error occurred.")
                except ConnectionError:
                    logger.exception(f"A Connection error occurred")
                    time.sleep(30)
                    continue
                break
    create_books_json(books, namespace)


if __name__ == '__main__':
    main()
