from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Transaction, TransactionType, Card
from ..schemas import TransactionIn, TransactionOut
from ..security import get_current_user_id

router = APIRouter(prefix="/v1/transactions", tags=["transactions"])


@router.post("", response_model=TransactionOut)
def create_transaction(
    payload: TransactionIn,
    db: Session = Depends(get_db),
    uid: int = Depends(get_current_user_id),
):
    # Basic existence check for card
    card = db.get(Card, payload.card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    tx = Transaction(
        user_id=uid,
        card_id=payload.card_id,
        type=TransactionType(payload.type),
        quantity=payload.quantity,
        value_cents=payload.value_cents,
        value_type=payload.value_type,
        fee_cents=payload.fee_cents,
        marketplace=payload.marketplace,
        notes=payload.notes,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return TransactionOut.model_validate(tx.__dict__)
