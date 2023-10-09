# backend for Hackathon Lenta
[![Build Status](https://github.com/FirstLiners/Backend/actions/workflows/hackathon_lenta_workflow.yaml/badge.svg)](https://github.com/FirstLiners/Backend/actions/workflows/hackathon_lenta_workflow.yaml/)

## Описание:
API для проекта по созданию предсказательной модели и интерфейса по прогнозированию спроса на товары заказчика собственного производства ООО “Лента”.

## Технологии:
- Python 3.10
- Django 4.2.5
- Django REST Framework 3.14.0
- Postgres

## Для разработчиков:
#### Файл зависимостей:
"src/requirements.txt"

#### Пример файла с переменными среды:
".env.example"

#### Приложения:
- _api_: API;
- _config_: настройки проекта.
- users
- skus
- stores
- sales
- forecasts

#### Линтер:
- black

## Запуск приложения:
Для запуска приложения необходим `Docker`. Для операционной системы Windows необходимо установить и активировать WSL2 (https://docs.docker.com/desktop/wsl/).

```команды для запуска проекта
docker-compose up
```
Выполняется из корневой папки проекта.

После первого запуска проекта необходимо выполнить настройки:
```команды для настройки проекта
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
docker-compose exec backend python manage.py createsuperuser
```

Для загрузки данных необходимо выполнить следующие команды:
Загрузка данных о товарной иерархии:
```
docker-compose exec backend python manage.py import_skus
```
Загрузка данных о магазинах:
```
docker-compose exec backend python manage.py import_stores
```
Загрузка исторических данных о продажах:
```
docker-compose exec backend python manage.py import_sales
```
Загрузка уникальных пар товар-магазин:
```
docker-compose exec backend python manage.py upload_pairs
```

## Команда проекта:
- Пеньтюк Павел (github: https://github.com/PentiukPavel)
