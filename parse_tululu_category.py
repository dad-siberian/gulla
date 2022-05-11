import json
import argparse
import logging
import time
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


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page', nargs='?', type=int, required = True)
    parser.add_argument('--end_page', nargs='?', default=701, type=int)
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
    for page_number in tqdm(range(namespace.start_page, namespace.end_page)):
        fiction_url = f'https://tululu.org/l55/{page_number}/'
        soup = get_soup(fiction_url)
        book_urls = parse_book_urls(soup)
        for book_url in tqdm(book_urls):
            while True:
                try:
                    book = get_book(book_url)
                    books.append(book)
                except HTTPError:
                    logger.exception(f"An HTTP error occurred.")
                except ConnectionError:
                    logger.exception(f"A Connection error occurred")
                    time.sleep(30)
                    continue
                break
    with open('books.json', 'a') as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
