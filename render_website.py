import json
import logging.config
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

from log_config import LOGGING_CONFIG

logger = logging.getLogger(__file__)


def render_website():
    with open('books.json', 'r', encoding='utf-8') as file:
        books = json.load(file)

    folder_path = os.path.join('.', 'pages')
    os.makedirs(folder_path, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    for page_number, some_books in enumerate(chunked(books, 10)):
        template = env.get_template('template.html')
        rendered_page = template.render(books=some_books)
        filepath = os.path.join(folder_path, f'index{page_number}.html')
        with open(filepath, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    logging.config.dictConfig(LOGGING_CONFIG)
    render_website()
    server = Server()
    server.watch('template.html', render_website)
    server.serve(root='.')


if __name__ == '__main__':
    main()
