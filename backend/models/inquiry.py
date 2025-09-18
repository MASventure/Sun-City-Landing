from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


def _timestamp() -> datetime:
    return datetime.utcnow()


@dataclass
class Inquiry:
    """Represents a visitor tour request submitted through the landing page."""

    name: str
    email: str
    phone: str
    preferred_date: str
    message: Optional[str] = None
    created_at: datetime = field(default_factory=_timestamp)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "preferred_date": self.preferred_date,
            "message": self.message,
            "created_at": self.created_at.isoformat() + "Z",
        }
