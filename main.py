import argparse
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def download_txt(book_id, filename, folder='books/'):
    url = f'http://tululu.org/txt.php?id={book_id}'
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f'{book_id}. {filename}')
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    with open(f'{filepath}.txt', 'wb') as file:
        file.write(response.content)


def check_for_redirect(response):
    if response.url == 'https://tululu.org/':
        raise requests.HTTPError


def get_soup(book_id):
    url = f'https://tululu.org/b{book_id}'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return BeautifulSoup(response.text, 'lxml')


def parse_title_and_author(soup):
    title_tag = soup.find('body').find('h1').text.split('::')
    title = {
        'title': sanitize_filename(title_tag[0].strip()),
        'author': sanitize_filename(title_tag[1].strip()),
    }
    return title


def get_cover_url(soup):
    img_url = soup.find('div', class_='bookimage').find('img')['src']
    return urljoin('https://tululu.org', img_url)


def download_image(url, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    filename = os.path.basename(url)
    filepath = os.path.join(folder, filename)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def parse_comments(soup):
    comments = soup.find_all('div', class_='texts')
    return [comment.find('span').text for comment in comments]


def parse_genres(soup):
    genres = soup.find('span', class_='d_book').find_all('a')
    return [genre.text for genre in genres]


def parse_book_page(soup):
    book_page = {
        'title': parse_title_and_author(soup)['title'],
        'author': parse_title_and_author(soup)['author'],
        'genre': parse_genres(soup),
        'comments': parse_comments(soup),
    }
    return book_page


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_id', nargs='?', default=1, type=int)
    parser.add_argument('end_id', nargs='?', default=10, type=int)
    return parser



def main():
    parser = createParser()
    namespace = parser.parse_args()
    for book_id in range(namespace.start_id, namespace.end_id):
        try:
            soup = get_soup(book_id)
            cover_url = get_cover_url(soup)
            book_title = parse_title_and_author(soup)['title']
            download_txt(book_id, book_title)
            download_image(cover_url)
            parse_book_page(soup)
        except requests.HTTPError:
            print('redirect')


if __name__ == '__main__':
    main()
