# Kind Loans Application

## Setup

1. Install Docker
1. Run `docker compose build` to build the docker images
1. Run `docker compose up` to start the containers
1. Run `docker compose run --rm backend sh -c "python manage.py
   createsuperuser"` to create a superuser
1. Run `docker compose run --rm backend sh -c "python manage.py
   create_groups"` to generate the following groups: admin, lender, borrower
1. Run `docker compose run --rm backend sh -c "python manage.py generate_sample_data 2 6"` to generate sample data
1. Run `docker compose run --rm backend sh -c "python manage.py create_tags"` to create tags for loan profiles
1. Run `docker compose down` to stop the containers

## Backend

- Django
- Django Rest Framework
- PostgreSQL

- localhost:8000/admin - Django admin
- localhost:8000/docs - Django Rest Framework documentation

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

## Production SSL Setup

1. Ensure your server has a public IP address accessible from the internet
2. Test the SSL certificate generation first with dry-run:
   ```bash
   docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d example.org
   ```
3. After successful dry-run, generate the actual certificate:
   ```bash
   docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d example.org
   ```
4. Set up automatic renewal (certificates expire every 3 months):
   ```bash
   docker compose run --rm certbot renew
   ```
   Consider adding this command to a cron job to run monthly.

## Questions

- frontend: how do we leverage figma to (easily) create the frontend?

- backend:
  - what happens if the loan deadline is reached?
  - is loan duration related to loan-deadline?
  - implications of removing a loan profile?
    - before approval
    - after approval
    - while gathering funds
    - after funds are gathered
