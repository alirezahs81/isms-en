# Internet Services Management System (ISMS)

Internet service sales & subscription management system — English UI (LTR)

## ✨ Features

- 📊 **Dashboard**: overview stats, renewal reminders for services expiring within 14 days, unpaid invoices
- 👥 **Customer management**: create, edit, search, and full customer profile with services and invoices
- 📦 **Service plans**: three categories — Internet (ADSL/TD-LTE), Hosting/Domain/Server, Software Licenses — monthly to annual terms
- 🖥 **Service management**: register services, filter by status, one-click renewal, issue renewal invoices
- 🧾 **Invoices & payments**: auto-numbered invoices, discounts, payment recording (cash, card, online gateway, bank transfer), invoice cancellation — invoice status automatically becomes "Paid" once fully paid
- 📈 **Reports**: monthly income, receivables, services distribution by category
- 👤 **User management**: create admin/staff users (administrator only)
- 🔐 **Django admin panel**: full data management at `/admin/`

Access is restricted to admin/staff. English, left-to-right interface.

## 🛠 Tech Stack

- Python 3.15 / Django 6.1
- PostgreSQL 16
- HTML/CSS (no frontend framework)

## 🚀 Getting Started

```bash
# Install dependencies
pip install django psycopg2-binary

# Create the database in PostgreSQL
psql -U postgres -c "CREATE DATABASE isms;"

# Set environment variables (optional — defaults: isms/postgres@127.0.0.1:5432)
set ISMS_DB_NAME=isms
set ISMS_DB_USER=postgres
set ISMS_DB_PASSWORD=postgres

# Run migrations
python manage.py migrate

# Create an admin user
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

Then open your browser at `http://127.0.0.1:8000`

> **Note:** This English version shares the same database schema as the Persian version — the Persian UI edition lives in a separate repository.

## ⚙️ Environment Variables

| Variable | Default | Description |
|---|---|---|
| `ISMS_DB_NAME` | `isms` | Database name |
| `ISMS_DB_USER` | `postgres` | Database user |
| `ISMS_DB_PASSWORD` | `postgres` | Database password |
| `ISMS_DB_HOST` | `127.0.0.1` | Database host |
| `ISMS_DB_PORT` | `5432` | Database port |
| `ISMS_DEBUG` | `1` | Debug mode (set to `0` in production) |
| `ISMS_SECRET_KEY` | — | Django secret key |

## 📁 Project Structure

```
isms-en/
├── services/     # Customers, service plans, service orders
├── invoices/     # Invoices and payments
├── accounts/     # System user management
├── dashboard/    # Dashboard and reports
├── templates/    # English LTR templates
└── isms/         # Project settings
```

## 📄 License

MIT
