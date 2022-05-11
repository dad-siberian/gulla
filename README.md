# gulla

## Урок 3. Парсим онлайн-библиотеку

Парсер книг с сайта [tululu.org](https://tululu.org/). Электронные книги в библиотеке бесплатны. Скрипт скачивает книги в txt формате.

## Запуск

Для запуска программы требуется Python 3.

- Скачайте код

```
git clone https://github.com/dad-siberian/gulla.git
```

- Установите зависимости командой

```
pip install -r requirements.txt
```

- Для того что бы скачать книги запустите файл `parse_tululu_book.py` командой

```
python3 parse_tululu_book.py start_id end_id
```

Где `start_id` и `end_id` это начало и конец диапазона скачивания книг.

Например, команда:

`python3 parse_tululu_book.py 10 20`

скачает с 10 по 20 книги.

Скаченные книги лежат в папке books/. Программа так же скачивает обложки книг (папка images/).

- Для скачивания книг из жанра фантастики запустить файл `parse_tululu_category.py`

```
python3 parse_tululu_category.py --start_page --end_page
```

Где `--start_page` и `--end_page` это диапазон страниц каталога книг в жанре Научная фантастика.

Например, команда:

`python3 parse_tululu_category.py --start page 10 --end_page 15`
скачает книги (~90 штук) с 10 по 15 страниц каталога [tululu.org](https://tululu.org/l55/) 

У `parse_tululu_category.py` есть еще несколько не обязательных аргументов:

- `--dest_folder` — путь к каталогу с результатами парсинга: картинкам, книгам, JSON.
- `--skip_imgs` — не скачивать картинки
- `--skip_txt` — не скачивать книги
- `--json_path` — указать свой путь к \*.json файлу с результатами


## Цели проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
