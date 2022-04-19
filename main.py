import os

import requests


def download_books(file_path, book_id):
    url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    file_name = f'book_{book_id}.txt'
    with open(f'{file_path}{file_name}', 'wb') as file:
        file.write(response.content)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError

def main():
    file_path = 'books/'
    os.makedirs(file_path, exist_ok=True)
    for book_id in range(1, 11):
        try:
            download_books(file_path, book_id)
        except requests.HTTPError:
            print('redirect')


if __name__ == '__main__':
    main()
