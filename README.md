# messeger_nits
Выпускная работа NITS2021

Бекенд оффлайн мессенджера. Реализован на с БД SQLite. Docker не используется.

Требуется установить зависимости:
    pip install -r requirements.txt

Запуск файла: main.py

Конфигурация приложения осуществляется в файле .env в корневом каталоге.
Пример файла .env:

host = 'localhost'

port = 8000

workers = 1

debug = False

dbname = 'db.sqlite'