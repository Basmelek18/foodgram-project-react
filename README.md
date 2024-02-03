# FoodGram

# Описание:
FoodGram - сайт, на котором пользователи будут публиковать рецепты, добавлять чужие 
рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта 
также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, 
которые нужно купить для приготовления выбранных блюд.


# Инструкция как развернуть в докере

Открыть директорию в терминале foodgram-project-react\infra
```
docker compose up
```
После создания контейнеров в другом окне терминала foodgram-project-react\infra
```
docker compose exec backend python manage.py collectstatic
docker compose exec backend python manage.py migrate
```


# Стек технологий использованных в проекте:

- Python 3.9
- Django 3.2
- DRF 3.14.0
- Djoser
- Django Colorfield
- Postgres 
- Nginx

# Как наполнить БД данными:

Открыть директорию в терминале foodgram-project-react\infra
```
docker cp ../data/ingredients.csv <Имя бэкенд контейнера>:/data/
docker compose exec backend python manage.py import_csv
docker compose exec backend python manage.py createsuperuser
cp ../docs/ <Имя nginx контейнера>:/usr/share/nginx/html/api/

```

# Примеры работы с API для всех пользователей

### Документация к API

Документация находиться по адресу `http://localhost:9000/api/docs/`


# Автор:

- [Вячеслав Испанюк](https://github.com/Basmelek18)