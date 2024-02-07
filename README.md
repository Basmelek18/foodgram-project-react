# FoodGram

# Description:
FoodGram - A site where users can publish recipes, add other people's recipes to their favorites, and subscribe to other
authors. Users of the site will also have access to the "Shopping List" service.
It will allow to create a list of products, that need to be purchased for the preparation of selected dishes.


# Instructions on how to deploy in Docker

In directory foodgram-project-react\infra
```
docker compose up
```
After creating containers in another terminal window foodgram-project-react\infra
```
docker compose exec backend python manage.py collectstatic
docker compose exec backend python manage.py migrate
```


# Stack of technologies used in the project:

- Python 3.9
- Django 3.2
- DRF 3.14.0
- Djoser
- Django Colorfield
- Postgres 
- Nginx

# How to fill the database with data:

Open the directory in the terminal foodgram-project-react\infra
```
docker cp ../data/ingredients.csv <backend container name>:/data/
docker compose exec backend python manage.py import_csv
docker compose exec backend python manage.py createsuperuser
cp ../docs/ <Имя nginx контейнера>:/usr/share/nginx/html/api/

```

# Examples of working with API for all users

### API documentation

The documentation can be found at `http://localhost:9000/api/docs/`


# Author:

- [Ispaniuk Viacheslav](https://github.com/Basmelek18)