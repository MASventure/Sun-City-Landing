# CardStock Backend (MVP Starter)

A plug‑and‑play FastAPI backend with Docker Compose (Postgres + API) for:
- Auth (JWT)
- Transactions (buy/sell/trade)
- Portfolio (ROI, marks from latest price snapshot)
- Scan (stub endpoint to integrate your model)
- Limits (free vs premium placeholders)

## Quick Start (Docker)

```bash
cd cardstock-backend
docker compose up --build
```

API available at: http://localhost:8000 (see `/docs` for Swagger)

Postgres at: localhost:5432 (cardstock / postgres / postgres)

### Seed sample cards
Open a psql shell into the db container and run seed.sql:

```bash
docker compose exec -T db psql -U postgres -d cardstock < seed.sql
```

### Create a user and authenticate
In `/docs`:
1) `POST /v1/auth/signup` → copy the `token`
2) Click **Authorize** (top right) and paste: `Bearer <token>`

### Add price snapshots (so portfolio can mark positions)
Use your DB client or psql:
```sql
INSERT INTO price_snapshots (card_id, grade, source, price_cents, link)
VALUES (1,'RAW','ebay',25000,'https://example.com'),
       (2,'RAW','ebay',12000,'https://example.com'),
       (3,'RAW','ebay',18000,'https://example.com');
```

### Add transactions
`POST /v1/transactions`
```json
{
  "card_id": 1,
  "type": "BUY",
  "quantity": 1,
  "value_cents": 15000,
  "fee_cents": 500,
  "marketplace": "local"
}
```

### View portfolio
`GET /v1/portfolio`

## Env (optional without Docker)
Copy `.env.example` → `.env` and set `DATABASE_URL` etc.

## Notes
- This is intentionally minimal so you can extend quickly.
- Plug your recognition model into `POST /v1/scan`.
- Build ingestion workers to populate `price_snapshots` regularly.
- Limits endpoint returns simple placeholders; wire to real quotas next.
