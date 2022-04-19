import os
import requests

def download_books(file_path):
    for id in range(1, 11):
        url = f'https://tululu.org/txt.php?id={id}'
        response = requests.get(url)
        response.raise_for_status()
        filename = f'book_{id}.txt'
        with open(f'{file_path}{filename}', 'wb') as file:
            file.write(response.content)

def main():
    file_path = 'books/'
    os.makedirs(file_path, exist_ok=True)
    download_books(file_path)


if __name__ == '__main__':
    main()