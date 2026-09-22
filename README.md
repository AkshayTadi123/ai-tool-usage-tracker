# AI Tool Usage Tracker
 
A small internal tool for tracking AI coding-tool usage (tokens and cost) by user and team: browse and filter records, add new ones, see per-team totals.
 
Built over a weekend to get hands-on experience, before my interview, with the AMD Analytics team's stack —
Angular, FastAPI and MySQL!! 
 
**Stack:** Angular (standalone components, RxJS) · FastAPI + SQLAlchemy + Pydantic · MySQL 8 · Docker Compose
 
## API
 
| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/records?team=&limit=&offset=` | List records, filtered and paginated |
| POST | `/records` | Create a record (validated, returns 201) |
| GET | `/summary` | Total tokens and cost per team |
 
Schemas are at `/docs`, generated from the Pydantic models.
 
## Schema
 
```sql
CREATE TABLE usage_records (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_name VARCHAR(100)  NOT NULL,
  team      VARCHAR(100)  NOT NULL,
  tool      VARCHAR(50)   NOT NULL,
  tokens    INT           NOT NULL,
  cost      DECIMAL(10,2) NOT NULL,
  used_on   DATE          NOT NULL,
  INDEX idx_team_date (team, used_on)
);
```
 
## Design notes
 
- **Composite index on `(team, used_on)`** matches the main access pattern: filtering by team over a date range. Cost is `DECIMAL`, not float, to avoid rounding drift on money.
- **`/summary` aggregates in SQL**, not Python — push the work to where the data lives and return a handful of rows instead of thousands.
- **Request-scoped DB sessions** via FastAPI's `Depends`, so no shared global connection.
- **Angular services own all HTTP.** Components consume typed Observables from `UsageService` rather than calling `HttpClient` directly.
- **Data is synthetic**, generated with `faker`: ~25 users, 5 teams, 60 days, deliberately skewed toward a few heavy users so pagination and the summary show realistic behaviour.

## Running it
 
```bash
cp .env.example .env
docker compose up --build        # web :4200, api :8000
docker compose exec api python seed.py
```
