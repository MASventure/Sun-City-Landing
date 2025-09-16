from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint, Enum, Numeric, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Enum as SAEnum
from enum import Enum as PyEnum

from .db import Base

class PlanTier(str, PyEnum):
    FREE = "FREE"
    PREMIUM = "PREMIUM"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    plan_tier: Mapped[str] = mapped_column(SAEnum(PlanTier), default=PlanTier.FREE, nullable=False)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

class Card(Base):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(50))  # e.g., 'Pokemon', 'NBA'
    set_name: Mapped[str] = mapped_column(String(255))
    year: Mapped[str] = mapped_column(String(10))
    title: Mapped[str] = mapped_column(String(255))  # player/character + number/variant
    number: Mapped[str] = mapped_column(String(50), nullable=True)
    variant: Mapped[str] = mapped_column(String(120), nullable=True)

class TransactionType(str, PyEnum):
    BUY = "BUY"
    SELL = "SELL"
    TRADE_IN = "TRADE_IN"
    TRADE_OUT = "TRADE_OUT"
    ADJUSTMENT = "ADJUSTMENT"

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"), index=True)
    type: Mapped[str] = mapped_column(SAEnum(TransactionType), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    value_cents: Mapped[int] = mapped_column(Integer, default=0)  # cash or assigned value for trades
    value_type: Mapped[str] = mapped_column(String(10), default="cash")  # 'cash' or 'card'
    fee_cents: Mapped[int] = mapped_column(Integer, default=0)
    marketplace: Mapped[str] = mapped_column(String(50), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    ts: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    card = relationship("Card")

class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"
    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"), index=True)
    grade: Mapped[str] = mapped_column(String(20), nullable=True)  # e.g., 'RAW', 'PSA 10'
    source: Mapped[str] = mapped_column(String(50))
    price_cents: Mapped[int] = mapped_column(Integer)
    ts: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())
    link: Mapped[str] = mapped_column(String(500), nullable=True)
    raw_json: Mapped[str] = mapped_column(Text, nullable=True)

    card = relationship("Card")
