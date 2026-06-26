# Travel Planner

REST API for planning trips. You create a project, add places to it from the Art Institute of Chicago API, leave notes, and mark places as visited. When you visit everything the project is automatically marked as completed.

Built with Django + Django Ninja, PostgreSQL, and Docker.

---

## How to run

You need Docker installed. That's it.

```bash
cd travel_planner

make build
make up
```

In a separate terminal:

```bash
make migrate
```

Done. The API is running at http://localhost:8000/api/docs (Swagger UI).

If you want access to Django Admin:

```bash
make superuser
```

Then go to http://localhost:8000/admin/.

---

## What's inside

- `travel_planner/` — Django project settings, URL config, API setup
- `trips/` — the main app with models, views, schemas, and the Art Institute API service
- `envs/dev.env` — environment variables for local development
- `Dockerfile` + `docker-compose.yml` — everything to run with one command

---

## API

All endpoints are under `/api/trips/`. Full interactive docs are at `/api/docs`.

### Projects

- **POST** `/projects` — create a project with places (pass an array of `external_id` from the Art Institute API)
- **GET** `/projects` — list all projects (supports pagination and filtering by `is_completed`)
- **GET** `/projects/{id}` — get one project
- **PATCH** `/projects/{id}` — update name, description, or start date
- **DELETE** `/projects/{id}` — delete a project (won't work if any place is already visited)

### Places

- **POST** `/projects/{id}/places` — add a place to a project
- **GET** `/projects/{id}/places` — list places in a project (supports pagination and filtering by `is_visited`)
- **GET** `/projects/{id}/places/{place_id}` — get one place
- **PATCH** `/projects/{id}/places/{place_id}` — update notes or mark as visited

### Artworks

- **GET** `/artworks?q=monet` — search artworks in the Art Institute of Chicago API

---

## Quick examples

Create a project:

```bash
curl -X POST http://localhost:8000/api/trips/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chicago Art Tour",
    "description": "Famous artworks I want to see",
    "start_date": "2026-08-01",
    "places": [
      {"external_id": 27992},
      {"external_id": 28560}
    ]
  }'
```

Add notes to a place:

```bash
curl -X PATCH http://localhost:8000/api/trips/projects/1/places/1 \
  -H "Content-Type: application/json" \
  -d '{"notes": "Must see this one!"}'
```

Mark a place as visited:

```bash
curl -X PATCH http://localhost:8000/api/trips/projects/1/places/1 \
  -H "Content-Type: application/json" \
  -d '{"is_visited": true}'
```

---

## Rules and validations

- Each project must have **1 to 10 places**
- You can't add the same artwork twice to one project
- Every artwork is checked against the Art Institute API before saving — if it doesn't exist there, you'll get an error
- You **can't delete** a project if any of its places are already marked as visited
- When **all places** in a project are visited — the project is automatically completed
- Adding a new place to a completed project sets it back to not completed
- Art Institute API responses are **cached for 1 hour** so we don't spam their API

---

## Makefile commands

| Command          | What it does                  |
| ---------------- | ----------------------------- |
| `make build`     | Build Docker images           |
| `make up`        | Start everything              |
| `make down`      | Stop everything               |
| `make migrate`   | Run database migrations       |
| `make superuser` | Create admin user             |
| `make shell`     | Open Django shell in container|

---

## Tech stack

- Python 3.14
- Django 6 + Django Ninja
- PostgreSQL 16
- Docker & Docker Compose
- Poetry

---

## Environment variables

All in `envs/dev.env`. For local dev everything is already set up, you don't need to change anything.

### Django
```env
DEBUG=True
SECRET_KEY=your-secret-key
```

### PostgreSQL
```env
POSTGRES_DB=name_db
POSTGRES_USER=name_user
POSTGRES_PASSWORD=password
POSTGRES_HOST=name_host
POSTGRES_PORT=5432
```
