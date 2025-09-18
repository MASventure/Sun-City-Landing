from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..security import get_current_user_id
from ..utils_portfolio import compute_portfolio
from ..schemas import PortfolioOut, PortfolioHolding

router = APIRouter(prefix="/v1/portfolio", tags=["portfolio"])

@router.get("", response_model=PortfolioOut)
def get_portfolio(db: Session = Depends(get_db), uid: int = Depends(get_current_user_id)):
    data = compute_portfolio(db, uid)
    data['holdings'] = [PortfolioHolding(**h) for h in data['holdings']]
    return data
