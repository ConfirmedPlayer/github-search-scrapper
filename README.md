# github-search-scrapper

> Парсер результатов поиска с Github

# Установка и запуск
> На сервере на локалхосте должна быть создана база данных "github-search" в PostgreSQL\
> Также в переменных окружения должны присутстовать логин и пароль от БД и от аккаунта Github [(config.py)](https://github.com/ConfirmedPlayer/github-search-scrapper/blob/5975ed12d3773ef72d5057cee64079b23e636a02/github-search-scrapper/config.py)
* Склонируйте репозиторий
* Создайте виртуальное окружение в корневой директории:\
\
Через venv (по-умолчанию):
```shell
python -m venv venv
```
```shell
./venv/Scripts/activate
```
```shell
pip install .\requirements.txt
```
Запуск:
```shell
python .\main.py
```
✅\
\
Или через [Poetry](https://python-poetry.org/):
```shell
poetry shell
```
```shell
poetry install
```
Запуск:
```shell
python .\main.py
```
✅
