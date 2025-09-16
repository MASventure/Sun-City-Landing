from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Transaction, TransactionType, Card, PriceSnapshot

def compute_portfolio(db: Session, user_id: int):
    # Aggregate positions and cost basis from transactions
    # Simple average cost basis per card; for MVP we won't track lots
    txs = db.execute(
        select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.ts.asc())
    ).scalars().all()

    positions = {}  # card_id -> {'qty': int, 'cost': int, 'realized': int}
    for t in txs:
        pos = positions.setdefault(t.card_id, {'qty': 0, 'cost': 0, 'realized': 0})
        if t.type in (TransactionType.BUY, TransactionType.TRADE_IN, TransactionType.ADJUSTMENT):
            # Increase qty and cost (cash or assigned)
            pos['qty'] += t.quantity
            pos['cost'] += t.value_cents + t.fee_cents
        elif t.type in (TransactionType.SELL, TransactionType.TRADE_OUT):
            # Realize PnL using average cost
            if pos['qty'] <= 0:
                continue
            avg_cost_per = pos['cost'] / pos['qty'] if pos['qty'] else 0
            sell_cost = avg_cost_per * t.quantity
            proceeds = t.value_cents - t.fee_cents
            realized = proceeds - sell_cost
            pos['qty'] -= t.quantity
            pos['cost'] -= sell_cost
            positions[t.card_id] = pos
            pos['realized'] += int(realized)

    # Now compute marks from last price snapshot per card
    results = []
    invested = 0
    value_now = 0
    realized_total = 0
    for card_id, pos in positions.items():
        if pos['qty'] <= 0:
            realized_total += pos['realized']
            continue
        last_price = db.execute(
            select(PriceSnapshot.price_cents).where(PriceSnapshot.card_id == card_id).order_by(PriceSnapshot.ts.desc())
        ).scalars().first() or 0
        mark = last_price * pos['qty']
        unreal = int(mark - pos['cost'])
        invested += int(pos['cost'])
        value_now += int(mark)
        realized_total += pos['realized']
        title = db.execute(select(Card.title).where(Card.id == card_id)).scalar_one_or_none() or f"Card #{card_id}"
        results.append({
            "card_id": card_id,
            "title": title,
            "quantity": int(pos['qty']),
            "cost_basis_cents": int(pos['cost']),
            "mark_cents": int(mark),
            "unrealized_cents": unreal
        })

    unrealized_total = int(value_now - invested)
    return {
        "invested_cents": int(invested),
        "value_now_cents": int(value_now),
        "realized_cents": int(realized_total),
        "unrealized_cents": int(unrealized_total),
        "holdings": results
    }
