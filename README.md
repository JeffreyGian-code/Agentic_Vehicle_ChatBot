# Vehicle Agent with PostgreSQL

The application keeps its existing architecture:

```text
User -> LangChain agent -> SearchRequest -> search_vehicles tool
     -> VehicleService -> PostgreSQL -> list[Vehicle]
```

`Vehicle` represents a row stored in the database. `SearchRequest` represents
the optional filters produced by the LLM. PostgreSQL is reached only through
`VehicleService`; the tool never constructs SQL itself.

## 1. Install PostgreSQL and create the database

Install PostgreSQL for Windows, including the command-line tools. Open a new
PowerShell window and create a dedicated local application account:

```powershell
psql -U postgres -d postgres
```

At the `postgres=#` prompt, run the following. Choose your own strong local
password; do not use the example text literally.

```sql
CREATE ROLE vehicle_app LOGIN PASSWORD 'choose-a-strong-local-password';
CREATE DATABASE vehicle_agent OWNER vehicle_app;
\q
```

If PowerShell cannot find `psql`, add PostgreSQL's `bin` directory to PATH or
run its full path (for example, `C:\Program Files\PostgreSQL\17\bin\psql.exe`).

## 2. Create the table and load 200 vehicles

From the project directory, run:

```powershell
psql -U vehicle_app -d vehicle_agent -f database/schema.sql
psql -U vehicle_app -d vehicle_agent -f database/seed.sql
psql -U vehicle_app -d vehicle_agent -c "SELECT COUNT(*) FROM vehicles;"
```

The final command must return `200`. `database/seed.sql` contains 20 sensible
Indian-market model families and 10 trim levels each. It is deterministic and
idempotent for local development: it clears and replaces the `vehicles` table,
so do not run it against a database containing real production data.

## 3. Configure secrets safely

Copy the template and put your real values only in `.env`:

```powershell
Copy-Item .env.example .env
```

Set `DATABASE_URL` in `.env`:

```text
DATABASE_URL=postgresql://vehicle_app:your-url-encoded-password@localhost:5432/vehicle_agent
```

URL-encode password characters such as `@`, `:`, `/`, and `#`. `.env` is
ignored by Git; `.env.example` is intentionally safe to commit. Rotate any API
keys that have previously appeared in a terminal, chat, screenshot, or commit.

## 4. Install the PostgreSQL Python driver

With the project's virtual environment active:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirement.txt
```

The added dependency is `psycopg[binary]`, the PostgreSQL driver used by the
application.

## 5. Run and verify

```powershell
python -m pytest app/tests/test_vehicle_sevice.py
python main.py
```

Try: `Find Honda sedans under 12 lakh.` The LLM creates a validated
`SearchRequest`; `VehicleService` executes a parameterized query and returns
validated `Vehicle` objects. If PostgreSQL is not configured, the integration
test is skipped and the application reports a clear `DATABASE_URL` error when
it first searches.

## Notes on the implementation

- Queries use `%s` parameters rather than string interpolation, preventing SQL injection.
- Database connections are opened only for the service call and closed by context managers.
- The three commonly filtered fields have database indexes.
- Matching remains case-insensitive, preserving the behavior of the former JSON service.
- A small command-line app does not need a connection pool yet. Add one when moving to a long-running web/API deployment.
