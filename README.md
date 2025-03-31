# Kind Loans Application

## Setup

1. Install Docker
1. Run `docker compose build` to build the docker images
1. Run `docker compose up` to start the containers
1. Run `docker compose down` to stop the containers

## Backend

- Django
- Django Rest Framework
- PostgreSQL

- localhost:8000/admin - Django admin
- localhost:8000/docs - Django Rest Framework documentation

### Useful Commands

1. Run `docker compose run --rm backend sh -c "python manage.py
   createsuperuser"` to create a superuser
1. Run `docker compose run --rm backend sh -c "python manage.py
   create_tags"` to create tags for loan profiles
   
### Loading Database Fixtures (i.e. sample data)

1. Load sample data in order:
   
   (i.e loads groups: admin, volunteer, lender, borrower; users; loan_profiles: for borrower-users)
   
   ```

   docker compose run --rm backend sh -c "python manage.py loaddata users.json"
   docker compose run --rm backend sh -c "python manage.py loaddata loan_profiles.json"

   ```

### Notes on separation of models into apps

WARNING: This was a breaking change.

To fix:
1. Reset your database by removing docker volumes
   `docker compose down -v`
   `docker compose up --build -d`

1. Run django migrations again
   `docker compose run --rm backend sh -c "python manage.py migrate"`

These commands should resolve this issue.

## Frontend

- React
- Material UI

- Run `npm install` to install the dependencies so that your IDE can recognize them
- Don't run `npm start` as the frontend is served in the frontend container

- localhost:3000 - React application
