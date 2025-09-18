from fastapi import APIRouter, UploadFile, File, Depends
from ..security import get_current_user_id
from ..schemas import ScanOut

router = APIRouter(prefix="/v1", tags=["scan"])

@router.post("/scan", response_model=ScanOut)
async def scan_card(file: UploadFile = File(...), uid: int = Depends(get_current_user_id)):
    # MVP stub: return static candidates (you would plug your model here)
    # In production, save file to S3, run recognition, return top-k matches.
    return {
        "candidates": [
            {"card_id": 1, "title": "Pokemon 1999 Base Set Charizard #4 Holo", "confidence": 0.83, "variants": ["RAW","PSA 10","PSA 9"]},
            {"card_id": 2, "title": "NBA 2019 Prizm Ja Morant #249 Base", "confidence": 0.72, "variants": ["RAW","PSA 10","PSA 9"]},
            {"card_id": 3, "title": "Pokemon 1999 Base Set Blastoise #2 Holo", "confidence": 0.64, "variants": ["RAW","PSA 10","PSA 9"]},
        ]
    }
