CashFlow Pro

This project is designed to give you a solid FastAPI backend for tracking finances, with clear role-based access control and server-side rendering. It’s built to be maintainable and easy to follow, so you can handle user roles, manage income and expenses, process uploads like CSV and PDF, and always keep a log of critical actions.

Quick note on architecture: You get unified server-side rendering with FastAPI's Jinja2Templates, connected directly to a stateless API core.

Tech Stack

- Backend: FastAPI (Python)
- Database: SQLite (via SQLAlchemy ORM). You can swap out SQLite for PostgreSQL just by updating your connection string, thanks to SQLAlchemy’s abstraction.
- Auth: JWT stored in HTTPOnly cookies for secure SSR navigation; password hashing with bcrypt.
- Frontend: HTML5 + Tailwind CSS, directly built into Jinja2 templates.
- Document Processing: Native csv and pypdf modules.

Project Structure

finance-backend/
├── api/
│   ├── dependencies.py        # Handles JWT extraction and access decorators
│   ├── routes/                # Route controllers (auth, user, records, dashboard)
│   └── services/              # Business logic (document analyzer, etc.)
├── core/
│   ├── config.py              # Env settings, JWT constants
│   └── security.py            # Password hashing, token creation
├── db/
│   └── database.py            # SQLAlchemy setup
├── models/                    # ORM definitions
├── schemas/                   # Pydantic validation models
├── templates/                 # Jinja2 HTML templates
├── tests/                     # Pytest suite
├── web/
│   └── routes.py              # SSR template controllers
├── main.py                    # Entrypoint and router assembly
└── requirements.txt           # Dependencies list

API Reference

Swagger UI comes baked in and is ready at http://127.0.0.1:8000/docs while your server is running.

| Method | Endpoint                        | What It Does                                           | Who Can Use |
| ------ | ------------------------------- | ------------------------------------------------------ | ----------- |
| POST   | /api/auth/login                 | Authenticates user; returns HTTPOnly cookie            | Anyone      |
| POST   | /api/users/register             | Registers a new user                                   | Anyone      |
| GET    | /api/users/me                   | Returns profile of authenticated user                  | Any Auth    |
| POST   | /api/records/                   | Creates a new financial transaction                    | Admin Only  |
| GET    | /api/records/                   | Retrieves paginated transactions                       | Any Auth    |
| GET    | /api/dashboard/summary          | Shows current totals, savings rates, balances          | Any Auth    |
| POST   | /api/dashboard/reports/analyze  | Extracts data from uploaded CSV/PDFs                   | Any Auth    |

("Any Auth" just means any user who’s logged in and authenticated.)

Setup & Installation

1. Environment Setup
Copy the example env file to start off your local secrets:
cp .env.example .env

2. Install Dependencies
Make sure you've got Python 3.9+ ready.
python -m venv venv
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
pip install -r requirements.txt

3. Launch the Server
uvicorn main:app --reload

Go straight to http://127.0.0.1:8000/login and you’re in.

Admin Bootstrapping Security Note: For demo purposes, the first user you create through "Register Demo Admin" gets admin privileges by default. Don’t do this in production — use environment-seeded accounts or CLI migration scripts for admin setup.

Testing

You get a standard backend test suite powered by pytest and httpx. To run tests locally:
pytest
