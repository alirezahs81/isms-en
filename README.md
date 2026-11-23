# Internet Services Management System (ISMS)

An internet-service sales and subscription management system with an English, left-to-right (LTR) interface.

## Features

- **Dashboard:** overview statistics, renewal reminders for services expiring within 14 days, and unpaid invoices
- **Customer management:** create, edit, search, and view customer profiles with services and invoices
- **Service plans:** Internet (ADSL/TD-LTE), hosting/domain/server, and software licenses
- **Service management:** register services, filter by status, renew services, and issue renewal invoices
- **Invoices and payments:** automatic invoice numbering, discounts, payment recording, and invoice cancellation
- **Reports and users:** income and receivables reports, plus admin/staff user management
- **Django Admin:** data administration at `/admin/`

Administrative sections are restricted to authorized admin/staff users.

## Technology and tested versions

- Python **3.12** in CI
- Django dependency range from `requirements.txt`: `>=5.0,<7`
- PostgreSQL **16** in CI
- HTML/CSS

Django is not currently pinned to a specific patch release. Dependency installation selects an available compatible version within the declared range, so the exact installed Django version can change over time.

## Prerequisites

- Python 3.12
- PostgreSQL 16 (or a compatible PostgreSQL release)
- Git (optional, for cloning the repository)

## Setup on Windows PowerShell

Run the following commands from the project root.

### 1. Create a virtual environment and install dependencies

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, you can install dependencies using the virtual environment's Python directly without changing the execution policy:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Create the database

If the PostgreSQL command-line tools are installed, run:

```powershell
psql -U postgres -c "CREATE DATABASE isms;"
```

Skip this step if the database already exists.

### 3. Set environment variables for local development

In PowerShell:

```powershell
$env:ISMS_DB_NAME = "isms"
$env:ISMS_DB_USER = "postgres"
$env:ISMS_DB_PASSWORD = "your_database_password"
$env:ISMS_DB_HOST = "127.0.0.1"
$env:ISMS_DB_PORT = "5432"
$env:ISMS_DEBUG = "1"
$env:ISMS_SECRET_KEY = (python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
```

These variables apply only to the current PowerShell session. Set them again in each new session before running the application.

With `ISMS_DEBUG=1`, the settings allow a built-in development-only fallback key, although generating and using a random key as shown above is recommended. In the secure default mode (`ISMS_DEBUG=0`), `ISMS_SECRET_KEY` is required and the application will refuse to start without it.

### 4. Run migrations, create an administrator, and start the server

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

## Environment variables

| Variable | Code default | Description |
|---|---|---|
| `ISMS_DB_NAME` | `isms` | Database name |
| `ISMS_DB_USER` | `postgres` | Database user |
| `ISMS_DB_PASSWORD` | `postgres` | Database password; change it outside local development |
| `ISMS_DB_HOST` | `127.0.0.1` | Database host |
| `ISMS_DB_PORT` | `5432` | Database port |
| `ISMS_DEBUG` | `0` | Only the value `1` enables debug mode |
| `ISMS_SECRET_KEY` | unset | Required when debug mode is disabled |
| `ISMS_ALLOWED_HOSTS` | `localhost,127.0.0.1,testserver` | Comma-separated allowed host names |
| `ISMS_CSRF_TRUSTED_ORIGINS` | empty | Comma-separated trusted CSRF origins, including a scheme such as `https://example.com` |
| `ISMS_SECURE_SSL_REDIRECT` | `1` when debug is disabled | Redirect HTTP requests to HTTPS |
| `ISMS_HSTS_SECONDS` | `31536000` when debug is disabled | HSTS duration in seconds |

## Production configuration

- Set `ISMS_DEBUG=0` and provide a random, private `ISMS_SECRET_KEY` through your deployment environment or secret manager.
- Configure `ISMS_ALLOWED_HOSTS` and, when needed, `ISMS_CSRF_TRUSTED_ORIGINS` for the actual deployment domains.
- Replace the default database password.
- SSL redirect and HSTS are enabled by default when debug mode is disabled. Serve the application behind valid HTTPS and configure your reverse proxy appropriately.
- Never commit secrets to the Git repository.

## Continuous integration (CI)

GitHub Actions runs the following checks with Python 3.12 and PostgreSQL 16:
1. Install dependencies
2. Detect model changes without migrations using `python manage.py makemigrations --check --dry-run`
3. Apply migrations
4. Run `python manage.py check`
5. Run the test suite

A passing CI run does not replace deployment testing on the actual production infrastructure.

## Project structure

```
isms-en/
├── services/     # Customers, service plans, and service orders
├── invoices/     # Invoices and payments
├── accounts/     # User management
├── dashboard/    # Dashboard and reports
├── templates/    # English LTR templates
└── isms/         # Project settings
```

## License

MIT
