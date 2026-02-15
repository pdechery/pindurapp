# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pindurapp is a Flask REST API study project that manages relationships between Clients, Bars, and Bills. The application uses SQLAlchemy with a many-to-many relationship pattern through an association object.

## Technology Stack

- Python 3.11+ (3.13 in CI)
- Flask 3.1.2 with Application Factory pattern
- SQLAlchemy 2.0.44 (ORM with modern declarative mapping)
- Pydantic for request validation
- PostgreSQL as database
- Docker (nginx, flask via gunicorn, postgres)
- Gunicorn as WSGI server

## Application Architecture

### Module Structure

- `pindurapp/__init__.py` - Application factory, creates Flask app with instance-relative config
- `pindurapp/models.py` - SQLAlchemy ORM models (Client, Bar, Bills)
- `pindurapp/settings.py` - Default settings loaded from environment variables
- `instance/instance_settings.py` - Instance-specific secrets (SECRET_KEY, ALGORITHM)
- `pindurapp/views/` - Blueprint-based API routes using Flask MethodView (class-based views)
- `pindurapp/helpers/` - Utility functions for CLI commands and external services

### Database Models

The application uses an **association object pattern** (not a simple association table):

- **Bills** - Association object with composite primary key (client_id, bar_id) plus additional data (bill amount, timestamps)
- **Client** - Has one-to-many relationship with Bills, cascade deletes configured
- **Bar** - Has one-to-many relationship with Bills

The Bills model stores the bill amount for each client-bar relationship. When querying relationships:
- Use `client.bills` to get Bills objects (not Bar objects directly)
- Access the related entity via `bill.bar` or `bill.client`
- Example: `for bill in client.bills: print(bill.bar.name, bill.bill)`

### Configuration Loading

Settings are loaded in this order:
1. `pindurapp.settings.DefaultSettings` (from environment variables via python-dotenv)
2. `instance/instance_settings.py` (instance-specific overrides)

Required environment variables in `.env`:
- `DATABASE_URI` - PostgreSQL connection string
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` (for Docker)

## Development Commands

### Running the Application

**Local development:**
```bash
# Activate virtual environment first
source venv/bin/activate

# Run with Flask development server
flask --app pindurapp run

# Run with Gunicorn (production-like)
gunicorn --reload -w 2 pindurapp:app --bind 0.0.0.0:5000
```

**Docker:**
```bash
# Start all services (nginx, flask, postgres)
docker-compose up

# Run commands inside container
docker exec pindurapp-app-1 flask create-db
docker exec pindurapp-app-1 flask seed
```

### Database Commands

```bash
# Create all tables from models
flask create-db

# Drop all tables
flask drop-db

# Populate database with seed data (8 clients, 8 bars, 8 bills)
flask seed
```

### Testing and Linting

```bash
# Lint with flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Run tests with pytest (no tests currently exist in the project)
pytest
```

### Docker Helpers

```bash
# Connect to PostgreSQL inside container
docker exec -it pindurapp-postgres-1 psql -U postgres

# Test API endpoint (adjust IP as needed)
curl -i http://172.18.0.3:5000/api/clients
```

## API Endpoints

All endpoints use `/api` prefix and return JSON.

### Clients
- `GET /api/clients` - List all client names
- `GET /api/clients/<id>` - Get client details with all bills and related bars
- `POST /api/clients` - Create client with optional bills
- `PATCH /api/clients/<id>` - Add bills to existing client
- `DELETE /api/clients/<id>` - Delete client (cascades to bills)
- `GET /api/clients/sum` - Aggregate sum of bills per client

### Bars
- `GET /api/bars` - List all bars with bills and clients
- `GET /api/bars/<id>` - Get single bar details
- `POST /api/bars` - Create bar with optional clients/bills
- `PATCH /api/bars/<id>` - Add clients/bills to existing bar
- `DELETE /api/bars/<id>` - Delete bar

### Request Validation

All POST/PATCH requests are validated using Pydantic models defined in the view files. Validation errors return 500 status with error details.

## Code Patterns

### View Pattern
Views use Flask's `MethodView` class-based approach and are registered via blueprints:
```python
class MyAPI(MethodView):
    def get(self, id: int = None): ...
    def post(self): ...
    def patch(self, id): ...
    def delete(self, id): ...

blueprint.add_url_rule('/resource', view_func=MyAPI.as_view('api_name'))
```

### Database Queries
The codebase uses SQLAlchemy 2.0 style:
- Use `db.select()` for SELECT queries
- Execute with `db.session.execute(query)`
- Use `.scalar_one()`, `.scalars()`, or iterate results
- Use `db.get_or_404(Model, id)` for fetching by primary key

### Error Handling
- Use `abort(status_code, description="message")` for HTTP errors
- Global error handler converts HTTPException to JSON
- Database operations wrapped in try/except blocks

## Important Notes

- The application entry point is `pindurapp:app` (the app object in `pindurapp/__init__.py`)
- CORS headers are manually added with `Access-Control-Allow-Origin: *` in some endpoints
- Timezone is hardcoded to UTC-3 (Brazil) in models.py
- No automated tests exist yet, but CI is configured for pytest
- When working with Bills relationships, remember it's an association object pattern, not a simple many-to-many
