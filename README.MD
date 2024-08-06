# **orgstruct** - сервис для отображения структуру организации.

## Возможности сервиса:
- Отображения структуры организации на подготовленном семле данных
- Добавление пользователей через админку
- Кеширование структуры организации в бд

## Архитектура:
Сервис приложение (Django)  + PostgreSQL для хранения данных.  


## Для запуска сервиса необходимо:
Создать файл .env и определить в нем следующие переменные (файл заполнен тестовыми значениями): 
   * SECRET_KEY
   * DEBUG
   * POSTGRES_USER
   * POSTGRES_PASSWORD
   * POSTGRES_DB 
   * PG_HOST 
   * PG_PORT


### Ручной запуск:
- Установить зависимости из requirements.txt
- Запустить БД: docker-compose --env-file .\myorg\myorg\.env up pg
- Накатить миграции на бд: python manage.py migrate
- Заполнить данные для примера: python manage.py upload_data (загрузка тестовых данных с использованием FactoryBoy)
- Запустить сервирс: python manage.py runserver

### Запуск в докере:
- Выполнить: docker compose --env-file .\myorg\myorg\.env up

### Запуск тестов:
- Выполнить: python myorg\manage.py test myorg.apps.orgstruct


Открыть в браузере http://127.0.0.1:8000/orgstruct/hierarchy/

Задание https://docs.google.com/document/d/1mbZvp7GbTknanOjKF9IrPB7Zu4-tBnOHf09__HBLkqs/edit