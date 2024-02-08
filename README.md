# FoodGram

# Description:
FoodGram is a platform that empowers users to share their culinary creations, engage with a vibrant community, and discover a world of delightful recipes. Here's a refined description:

FoodGram is a culinary haven where users can unleash their creativity by sharing their favorite recipes with the community. The platform encourages users not only to showcase their culinary masterpieces but also to explore and appreciate the gastronomic delights crafted by fellow enthusiasts.

##Key Features:

###Recipe Publication:

-Users have the opportunity to publish their own unique recipes, adding a personal touch to the diverse collection on FoodGram.
Favorites Repository:

-Enabling a sense of culinary camaraderie, users can curate their own collection by adding recipes from other contributors to their favorites.
Author Subscriptions:

-To stay connected and inspired, users can subscribe to their favorite authors, ensuring they never miss out on new and exciting culinary adventures.

###Shopping List Service:

FoodGram extends its functionality with a convenient "Shopping List" service. Users can compile lists of ingredients required for specific dishes, streamlining the preparation process.
Whether you're a seasoned chef or a passionate home cook, FoodGram offers a dynamic space to share, savor, and connect through the joy of cooking. Join our community and embark on a flavorful journey where each recipe tells a unique story, and every user contributes to the rich tapestry of culinary experiences. Happy cooking!


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
