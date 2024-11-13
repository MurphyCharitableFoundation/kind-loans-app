# Kind Loans Application

## Setup

- 1. Install Docker
- 2. Run `docker compose build` to build the docker images
- 3. Run `docker compose run --rm backend sh -c "python manage.py createsuperuser"` to create a superuser
- 4. Run `docker compose run --rm backend sh -c "python manage.py generate_sample_data 2 6` to generate sample data
- 5. Run `docker compose up` to start the containers
- 6. Run `docker compose down` to stop the containers

## Backend

- Django
- Django Rest Framework
- PostgreSQL

- localhost:8000/admin - Django admin
- localhost:8000/docs - Django Rest Framework documentation

## Frontend

- React
- Material UI

- Run `npm install` to install the dependencies so that your IDE can recognize them
- Don't run `npm start` as the frontend is served in the frontend container

- localhost - React application

## Questions

- frontend: how do we leverage figma to (easily) create the frontend?

- backend: what happens if the loan deadline is reached?
- backend: implications of removing a loan profile?
    - before approval
    - after approval
    - while gathering funds
    - after funds are gathered
- backend: is loan duration related to loan-deadline?

- paypal-integration:
    Paypal Developer has a few [APIs](https://developer.paypal.com/api/rest/current-resources/) that we can work with.

    Both these examples need you to create a paypal dev account and transactions
    can be mocked in the Paypal Sandbox:
    - [backend integration example](https://www.youtube.com/watch?v=IXxEdhA7fig)
    - [frontend integration example](https://www.youtube.com/watch?v=f7NWToOjtKI)

    [Project specific paypal integration material available](./PAYPAL-INTEGRATION-NOTES.md)
