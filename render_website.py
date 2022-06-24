import json
import logging.config
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

from log_config import LOGGING_CONFIG

logger = logging.getLogger(__file__)


def render_website():
    with open('books.json', 'r', encoding='utf-8') as file:
        books = json.load(file)

    book_files = os.listdir('books')
    book_paths = list(map(lambda name: os.path.join('books', name), book_files))
    book_paths.sort()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        books=zip(books, book_paths)
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    logging.config.dictConfig(LOGGING_CONFIG)
    render_website()
    server = Server()
    server.watch('template.html', render_website)
    server.serve(root='.')


if __name__ == '__main__':
    main()
