export DB_ENGINE=${{ secrets.DB_ENGINE }}
export POSTGRES_DB=${{ secrets.POSTGRES_DB }}
export POSTGRES_USER=${{ secrets.POSTGRES_USER }}
export POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }}
export DB_HOST=${{ secrets.DB_HOST }}
export DB_PORT=${{ secrets.DB_PORT }}
export DJANGO_SECRET_KEY=${{ secrets.DJANGO_SECRET_KEY }}
docker compose up --no-recreate -d
docker compose up --no-deps -d web
docker compose exec web python manage.py collectstatic --no-input
docker compose exec web python manage.py migrate