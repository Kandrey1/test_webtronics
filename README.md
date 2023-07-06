# Тестовое задание
Задание в файле: Test Task for Webtronics FastAPI candidate.pdf

## Технологий
 - Python, FastAPI, SQLAlchemy, Postgres 
    

## Реализовано
- Регистрация и авторизация.
- Раздел Статьи (CRUD)
- Возможность голосовать (like/dislike)

Документация `http://127.0.0.1:8015/docs`


## Установка и запуск

На базе файла .env_sample создать файл .env

Находясь в корне проекта выполнить: 

`docker-compose up --build -d`

При первом запуске потребуется время на создание БД.
В это время приложение может выдавать ошибку(контейнер запустится с ошибкой, тогда необходимо
перезапустить контейнер с приложением:

`docker-compose down` 

`docker-compose up -d`
).

### Просмотр БД
Для удобства работы с БД, устанавливается pgAdmin по адресу `http://localhost:5050/browser/`
(необходимо дождаться установки и запуска)

- После запуска pgAdmin необходимо войти в него использую email и password
заданный в файле `.env`.

- Создать сервер и подключится к БД. Данные для подключения те же 
что и в файле `.env`.

### Тестирование
Установить зависимости `pip install -r requirements-dev.txt`

В БД Postgres необходимо создать БД с именем указанным в 
переменной POSTGRES_DB_TEST в файле .env

В .env `POSTGRES_HOSTNAME=postgres` заменить на `POSTGRES_HOSTNAME=localhost`

Для запуска тестов: `pytest tests`