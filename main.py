import os

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


def get_title_book(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('body').find('h1').text.split('::')
    return sanitize_filename(title_tag[0].strip())
    # print(f'Автор: {title_tag[1].strip()}')


def main():
    for book_id in range(1, 11):
        book_title = get_title_book(book_id)
        try:
            download_txt(book_id, book_title)
        except requests.HTTPError:
            print('redirect')


if __name__ == '__main__':
    main()
