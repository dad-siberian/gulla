import json
import logging
import time
from urllib.parse import urljoin

from requests import ConnectionError, HTTPError
from tqdm import tqdm

from parse_tululu_book import get_book, get_soup


logger = logging.getLogger('Logger')


def parse_book_urls(soup):
    base_url = 'https://tululu.org/'
    book_urls = list()
    book_hyperlinks = soup.select('div.bookimage a')
    for link in book_hyperlinks:
        book_href = link.get('href')
        book_urls.append(urljoin(base_url, book_href))
    return book_urls


def main():
    books = list()
    for page_number in tqdm(range(1, 5)):
        fiction_url = f'https://tululu.org/l55/{page_number}/'
        while True:
            try:
                soup = get_soup(fiction_url)
                book_urls = parse_book_urls(soup)
                for book_url in tqdm(book_urls):
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
