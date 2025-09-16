from fastapi import FastAPI
from .db import Base, engine
from .routes import auth, limits, transactions, portfolio, scan

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CardStock API (MVP)")

app.include_router(auth.router)
app.include_router(limits.router)
app.include_router(transactions.router)
app.include_router(portfolio.router)
app.include_router(scan.router)

@app.get("/health")
def health():
    return {"ok": True}
