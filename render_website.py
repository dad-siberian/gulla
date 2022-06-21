import logging.config
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

from log_config import LOGGING_CONFIG

logger = logging.getLogger(__file__)


def main():
    logging.config.dictConfig(LOGGING_CONFIG)

    with open('books.json', 'r', encoding='utf-8') as file:
        books = json.load(file)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(books=books)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    main()
