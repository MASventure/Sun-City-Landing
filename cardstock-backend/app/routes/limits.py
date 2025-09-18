import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from ..db import get_db
from ..models import Transaction, User
from ..security import get_current_user_id

router = APIRouter(prefix="/v1/me", tags=["limits"])

FREE_SCAN_LIMIT = int(os.environ.get("FREE_SCAN_LIMIT", "20"))
FREE_TRACK_LIMIT = int(os.environ.get("FREE_TRACK_LIMIT", "15"))
PREMIUM_SCAN_LIMIT = int(os.environ.get("PREMIUM_SCAN_LIMIT", "100000"))
PREMIUM_TRACK_LIMIT = int(os.environ.get("PREMIUM_TRACK_LIMIT", "100000"))


@router.get("/limits")
def get_limits(db: Session = Depends(get_db), uid: int = Depends(get_current_user_id)):
    user = db.get(User, uid)
    if user.plan_tier == "PREMIUM":
        return {
            "scans_remaining": PREMIUM_SCAN_LIMIT,
            "track_limit": PREMIUM_TRACK_LIMIT,
            "tracked_count": 0,
        }
    else:
        # tracked_count approximated: unique card_ids in transactions with net qty > 0
        # (simple version; precise count comes from positions calc)
        tracked_count = (
            db.execute(
                select(func.count(func.distinct(Transaction.card_id))).where(
                    Transaction.user_id == uid
                )
            ).scalar()
            or 0
        )
        return {
            "scans_remaining": FREE_SCAN_LIMIT,
            "track_limit": FREE_TRACK_LIMIT,
            "tracked_count": int(tracked_count),
        }
