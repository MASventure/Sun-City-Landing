from pydantic import BaseModel, EmailStr
from typing import Optional, List, Literal
from datetime import datetime


class SignupIn(BaseModel):
    email: EmailStr
    password: str


class AuthOut(BaseModel):
    token: str
    user_id: int


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TransactionIn(BaseModel):
    card_id: int
    type: Literal["BUY", "SELL", "TRADE_IN", "TRADE_OUT", "ADJUSTMENT"]
    quantity: int = 1
    value_cents: int = 0
    value_type: Literal["cash", "card"] = "cash"
    fee_cents: int = 0
    marketplace: Optional[str] = None
    notes: Optional[str] = None


class TransactionOut(BaseModel):
    id: int
    card_id: int
    type: str
    quantity: int
    value_cents: int
    fee_cents: int
    marketplace: Optional[str]
    notes: Optional[str]
    ts: datetime


class PortfolioHolding(BaseModel):
    card_id: int
    title: str
    quantity: int
    cost_basis_cents: int
    mark_cents: int
    unrealized_cents: int


class PortfolioOut(BaseModel):
    invested_cents: int
    value_now_cents: int
    realized_cents: int
    unrealized_cents: int
    holdings: List[PortfolioHolding]


class ScanOut(BaseModel):
    candidates: list
