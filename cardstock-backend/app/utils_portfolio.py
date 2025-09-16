from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Sequence

from sqlalchemy.orm import Session
from sqlalchemy import select, func

from .models import Transaction, TransactionType, Card, PriceSnapshot

_POSITIVE_TYPES = {
    TransactionType.BUY,
    TransactionType.TRADE_IN,
    TransactionType.ADJUSTMENT,
}
_NEGATIVE_TYPES = {
    TransactionType.SELL,
    TransactionType.TRADE_OUT,
}


def _quantize_to_cents(value: Decimal) -> int:
    """Round a decimal monetary amount (already expressed in cents) to an int."""

    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _latest_price_map(db: Session, card_ids: Sequence[int]) -> Dict[int, int]:
    """Return the most recent price snapshot in cents for each card."""

    if not card_ids:
        return {}

    ranked_prices = (
        select(
            PriceSnapshot.card_id.label("card_id"),
            PriceSnapshot.price_cents.label("price_cents"),
            func.row_number()
            .over(
                partition_by=PriceSnapshot.card_id,
                order_by=PriceSnapshot.ts.desc(),
            )
            .label("rnk"),
        )
        .where(PriceSnapshot.card_id.in_(card_ids))
        .subquery()
    )

    rows = db.execute(
        select(ranked_prices.c.card_id, ranked_prices.c.price_cents).where(
            ranked_prices.c.rnk == 1
        )
    )
    return {card_id: price for card_id, price in rows}


def compute_portfolio(db: Session, user_id: int):
    tx_rows = db.execute(
        select(
            Transaction.card_id,
            Transaction.type,
            Transaction.quantity,
            Transaction.value_cents,
            Transaction.fee_cents,
        )
        .where(Transaction.user_id == user_id)
        .order_by(Transaction.ts.asc())
    ).all()

    positions: Dict[int, Dict[str, Decimal | int]] = {}
    for card_id, tx_type, quantity, value_cents, fee_cents in tx_rows:
        pos = positions.setdefault(
            card_id,
            {"qty": 0, "cost": Decimal(0), "realized": Decimal(0)},
        )

        qty = int(quantity or 0)
        value = Decimal(value_cents or 0)
        fees = Decimal(fee_cents or 0)

        if tx_type in _POSITIVE_TYPES:
            pos["qty"] += qty
            pos["cost"] += value + fees
        elif tx_type in _NEGATIVE_TYPES:
            if qty <= 0 or pos["qty"] <= 0:
                continue

            sell_qty = min(pos["qty"], qty)
            if sell_qty <= 0:
                continue

            avg_cost_per = pos["cost"] / Decimal(pos["qty"])
            sell_cost = avg_cost_per * Decimal(sell_qty)
            proceeds = value - fees
            if qty != sell_qty:
                proceeds *= Decimal(sell_qty) / Decimal(qty)

            pos["qty"] -= sell_qty
            pos["cost"] -= sell_cost
            pos["realized"] += proceeds - sell_cost

            if pos["qty"] == 0:
                # Avoid carrying fractional pennies for fully exited positions.
                pos["cost"] = Decimal(0)

    active_card_ids = [cid for cid, pos in positions.items() if pos["qty"] > 0]
    latest_prices = _latest_price_map(db, active_card_ids)

    title_map: Dict[int, str] = {}
    if active_card_ids:
        rows = db.execute(select(Card.id, Card.title).where(Card.id.in_(active_card_ids)))
        title_map = {card_id: title for card_id, title in rows}

    holdings = []
    for card_id in active_card_ids:
        pos = positions[card_id]
        qty = int(pos["qty"])
        cost_dec = pos["cost"]
        mark_dec = Decimal(latest_prices.get(card_id, 0)) * Decimal(qty)
        unreal_dec = mark_dec - cost_dec

        holdings.append(
            {
                "card_id": card_id,
                "title": title_map.get(card_id, f"Card #{card_id}"),
                "quantity": qty,
                "cost_basis_cents": _quantize_to_cents(cost_dec),
                "mark_cents": _quantize_to_cents(mark_dec),
                "unrealized_cents": _quantize_to_cents(unreal_dec),
            }
        )

    invested_cents = sum(h["cost_basis_cents"] for h in holdings)
    value_now_cents = sum(h["mark_cents"] for h in holdings)
    unrealized_cents = sum(h["unrealized_cents"] for h in holdings)
    realized_total = sum((pos["realized"] for pos in positions.values()), Decimal(0))

    return {
        "invested_cents": invested_cents,
        "value_now_cents": value_now_cents,
        "realized_cents": _quantize_to_cents(realized_total),
        "unrealized_cents": unrealized_cents,
        "holdings": holdings,
    }
