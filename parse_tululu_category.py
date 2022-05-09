import logging
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

logger = logging.getLogger('Logger')


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return BeautifulSoup(response.text, 'lxml')


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def parse_book_urls(soup):
    base_url = 'https://tululu.org/'
    book_urls = []
    books = soup.find_all('div', class_='bookimage')
    for book in books:
        book_url = book.find('a').get('href')
        book_urls.append(urljoin(base_url, book_url))
    return book_urls


def parse_category(start, end):
    book_urls = []
    for page_number in tqdm(range(start, end)):
        fiction_url = f'https://tululu.org/l55/{page_number}/'
        while True:
            try:
                fiction_soup = get_soup(fiction_url)
                some_book_urls = parse_book_urls(fiction_soup)
                book_urls.extend(some_book_urls)
            except requests.HTTPError:
                logger.exception(f"An HTTP error occurred.")
            except requests.exceptions.ConnectionError:
                logger.exception(f"A Connection error occurred")
                time.sleep(30)
                continue
            break
    return book_urls
