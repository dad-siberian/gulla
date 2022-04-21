# gulla

Урок 3. Парсим онлайн-библиотеку
Парсер книг с сайта [tululu.org](https://tululu.org/). Электронные книги в библиотеке бесплатны. Скрипт скачивает книги в txt формате.


## Запуск

Для запуска программы требуется Python 3.

- Скачайте код `git clone https://github.com/dad-siberian/gulla.git`
- Установите зависимости командой `pip install -r requirements.txt`
- Запустите скрипт командой `python3 main.py start_id end_id`


Где `start_id` и `end_id` это начало и конец диапазона скачивания книг. 

Например, команда:

`python3 main.py 10 20`

скачает с 10 по 20 книги.

Скаченные книги лежат в папке books/. Программа так же скачивает обложки книг (папка images/).
В консоле выводится информация о скаченных книгах: Название, автор, жанр и отзывы.


## Цели проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
