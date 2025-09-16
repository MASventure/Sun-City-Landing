import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func, case
from ..db import get_db
from ..models import User, PlanTier, Transaction, TransactionType
from ..security import get_current_user_id

router = APIRouter(prefix="/v1/me", tags=["limits"])

FREE_SCAN_LIMIT = int(os.environ.get("FREE_SCAN_LIMIT", "20"))
FREE_TRACK_LIMIT = int(os.environ.get("FREE_TRACK_LIMIT", "15"))
PREMIUM_SCAN_LIMIT = int(os.environ.get("PREMIUM_SCAN_LIMIT", "100000"))
PREMIUM_TRACK_LIMIT = int(os.environ.get("PREMIUM_TRACK_LIMIT", "100000"))

_POSITIVE_TYPES = (
    TransactionType.BUY,
    TransactionType.TRADE_IN,
    TransactionType.ADJUSTMENT,
)
_NEGATIVE_TYPES = (
    TransactionType.SELL,
    TransactionType.TRADE_OUT,
)

def _tracked_cards_count(db: Session, uid: int) -> int:
    """Return how many cards the user currently tracks (net quantity > 0)."""

    qty_delta = func.sum(
        case(
            (Transaction.type.in_(_POSITIVE_TYPES), Transaction.quantity),
            (Transaction.type.in_(_NEGATIVE_TYPES), -Transaction.quantity),
            else_=0,
        )
    )

    tracked_cards = (
        select(Transaction.card_id)
        .where(Transaction.user_id == uid)
        .group_by(Transaction.card_id)
        .having(qty_delta > 0)
        .subquery()
    )

    count = db.scalar(select(func.count()).select_from(tracked_cards))
    return int(count or 0)


@router.get("/limits")
def get_limits(db: Session = Depends(get_db), uid: int = Depends(get_current_user_id)):
    user = db.get(User, uid)
    tracked_count = _tracked_cards_count(db, uid)

    if user and user.plan_tier == PlanTier.PREMIUM:
        return {
            "scans_remaining": PREMIUM_SCAN_LIMIT,
            "track_limit": PREMIUM_TRACK_LIMIT,
            "tracked_count": tracked_count,
        }

    return {
        "scans_remaining": FREE_SCAN_LIMIT,
        "track_limit": FREE_TRACK_LIMIT,
        "tracked_count": tracked_count,
    }
