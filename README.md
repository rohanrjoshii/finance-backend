# CashFlow Pro

A clear, maintainable FastAPI backend engineered for financial data processing, role-based access control, and server-side rendering.

## Overview
CashFlow Pro is a financial tracking API and dashboard. The system manages user roles (Admin, Analyst, Viewer), handles typical financial records (income, expenses), generates analytical summaries from structural document uploads (CSV/PDF) using explicit Python parsers, and logs all critical actions.

*Note on Architecture*: This project utilizes FastAPI's `Jinja2Templates` for unified Server-Side Rendering (SSR) built tightly around a stateless API architecture.

## Tech Stack
* **Backend:** FastAPI (Python)
* **Database:** SQLite with SQLAlchemy ORM. *(Note: SQLite is configured here for seamless single-instance development. The abstraction layer via SQLAlchemy allows for an instant swap to PostgreSQL via connection string updates).*
* **Authentication:** JWT via HTTPOnly Cookies (enabling robust SSR navigation) and `bcrypt` password hashing.
* **Frontend:** HTML5 / Tailwind CSS (CDN) embedded directly in Jinja2 templates.
* **Document Processing:** Python's native `csv` and `pypdf`.

---

## Project Structure
```text
finance-backend/
├── api/
│   ├── dependencies.py      # JWT extraction and Role-Based access decorators
│   ├── routes/              # FastAPI route controllers (auth, users, records, dashboard)
│   └── services/            # Business logic (e.g., document_analyzer.py)
├── core/
│   ├── config.py            # Environment settings and JWT constants
│   └── security.py          # Password hashing and token generation
├── db/
│   └── database.py          # SQLAlchemy engine and session dependency
├── models/                  # SQLAlchemy ORM definitions (record.py, user.py)
├── schemas/                 # Pydantic models for request/response validation
├── templates/               # Jinja2 HTML templates for SSR
├── tests/                   # Pytest suite
├── web/
│   └── routes.py            # Jinja2 template controllers
├── main.py                  # Application entry point and router assembly
└── requirements.txt         # Project dependencies
```

---

## API Endpoints Overview
A comprehensive, interactive Swagger UI is built into the framework and available at `http://127.0.0.1:8000/docs` while the server is running.

| Method | Endpoint                        | Description                                         | Access Level         |
| :---   | :---                            | :---                                                | :---                 |
| `POST` | `/api/auth/login`               | Authenticates a user and returns an HTTPOnly Cookie | Public               |
| `POST` | `/api/users/register`           | Registers a new user.                               | Public               |
| `GET`  | `/api/users/me`                 | Returns the currently authenticated user's profile  | Any Auth             |
| `POST` | `/api/records/`                 | Logs a new financial transaction                    | Admin Only           |
| `GET`  | `/api/records/`                 | Retrieves paginated transaction records             | Any Auth             |
| `GET`  | `/api/dashboard/summary`        | Returns current totals, savings rates, and balances | Any Auth             |
| `POST` | `/api/dashboard/reports/analyze`| Parses and extracts data from uploaded CSV/PDFs     | Any Auth             |

*(Note: "Any Auth" implies any successfully authenticated user role).*

---

## Setup & Installation

### 1. Environment Configuration
Copy the provided environment template to establish your local secrets.
```bash
cp .env.example .env
```

### 2. Install Dependencies
Ensure Python 3.9+ is installed.
```bash
python -m venv venv
# Activate the environment (Mac/Linux)
source venv/bin/activate  
# Activate the environment (Windows)
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Run the Server
```bash
uvicorn main:app --reload
```
Navigate directly to `http://127.0.0.1:8000/login` to access the application.

*Security Note on Admin Bootstrapping*: For demonstration purposes solely, the application natively grants `Admin` privileges to the very first user created via the "Register Demo Admin" button. Production systems should strictly rely on environment-seeded admin accounts or isolated CLI migration scripts.

---

## Testing
The application includes a standard backend test suite powered by `pytest` and `httpx`.
Run the verification suite locally using:
```bash
pytest
```
