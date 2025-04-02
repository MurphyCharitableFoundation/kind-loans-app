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

1. Auto: Run management command:

   ```

   docker compose run --rm backend sh -c "python manage.py loan_flow"

   ```

1. Manual: Load fixtures in order:

   For finer control over data evolution, load fixtures one by one and
   watch how the application data evolves from the admin console or
   using a JSON interface or frontend.
   
   ```

   docker compose run --rm backend sh -c "python manage.py loaddata users.json"
   docker compose run --rm backend sh -c "python manage.py loaddata loan_profiles.json"
   docker compose run --rm backend sh -c "python manage.py loaddata fund_lenders.json"
   docker compose run --rm backend sh -c "python manage.py loaddata lenders_contribute.json"
   docker compose run --rm backend sh -c "python manage.py loaddata pay_borrowers.json"
   docker compose run --rm backend sh -c "python manage.py loaddata borrowers_repay.json"
   docker compose run --rm backend sh -c "python manage.py loaddata apply_repayments.json"
   docker compose run --rm backend sh -c "python manage.py loaddata lenders_withdraw.json"

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
