# Lunch Voting Service

A Django REST Framework backend for internal lunch voting. Restaurants upload a daily menu, employees vote before lunch, and the API exposes the current day's menus and voting results.

## Stack

- Python 3.13
- Django + Django REST Framework
- JWT authentication (`djangorestframework-simplejwt`)
- PostgreSQL for Docker/local production-like runs
- Docker Compose
- Pytest
- Flake8

## API Versioning

The mobile application sends its version in headers. The service supports:

- `X-API-Version: 1` — a user can vote once per day and cannot change that vote.
- `X-API-Version: 2` — a user can change their vote during the same day; the latest choice is counted.

For compatibility the backend also accepts `Build-Version` and `X-Build-Version`. Missing or invalid versions default to version 2.

## Running with Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

The API will be available at `http://localhost:8000/api/`.

Create an admin user in another terminal:

```bash
docker compose exec api python manage.py createsuperuser
```

## Running locally without Docker

Install dependencies and run migrations:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Without `DATABASE_URL`, local runs use SQLite for convenience. Docker Compose uses PostgreSQL via `.env.example`.

## API Documentation

Interactive API documentation is available when the service is running:

- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI schema: `http://localhost:8000/api/schema/`
- ReDoc: `http://localhost:8000/api/redoc/`

Click **Authorize** in Swagger UI and provide `Bearer <access-token>` after obtaining a JWT token.

## Authentication

Obtain a JWT token:

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"your-password"}'
```

Use the returned access token:

```bash
curl http://localhost:8000/api/menus/today/ \
  -H 'Authorization: Bearer <access-token>' \
  -H 'X-API-Version: 2'
```

## Main Endpoints

| Method | Path | Description | Permission |
| --- | --- | --- | --- |
| `POST` | `/api/auth/token/` | Obtain JWT tokens | Public |
| `POST` | `/api/auth/token/refresh/` | Refresh JWT access token | Public |
| `POST` | `/api/employees/` | Create employee login/profile | Admin |
| `GET` | `/api/employees/` | List employees | Admin |
| `POST` | `/api/restaurants/` | Create restaurant | Admin |
| `GET` | `/api/restaurants/` | List restaurants | Authenticated |
| `POST` | `/api/menus/` | Upload/create a daily menu | Admin |
| `GET` | `/api/menus/today/` | Get current day menus | Authenticated |
| `POST` | `/api/votes/` | Vote for a menu | Authenticated |
| `GET` | `/api/votes/results/` | Get current day results | Authenticated |

## Example Menu Upload

```bash
curl -X POST http://localhost:8000/api/menus/ \
  -H 'Authorization: Bearer <access-token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "restaurant_id": 1,
    "date": "2026-05-06",
    "items": [
      {"name": "Chicken soup", "price": "7.50"},
      {"name": "Veggie bowl", "price": "11.00"}
    ]
  }'
```

## Testing and Linting

```bash
pytest
flake8
```
