from __future__ import annotations

from typing import List

from backend.models.inquiry import Inquiry


class InquiryService:
    """Store and retrieve inquiries in memory.

    In a production environment this would integrate with a persistent data store
    or messaging queue. The in-memory implementation is suitable for baseline
    development and automated testing.
    """

    def __init__(self) -> None:
        self._inquiries: List[Inquiry] = []

    def add_inquiry(self, inquiry: Inquiry) -> Inquiry:
        self._inquiries.append(inquiry)
        return inquiry

    def list_inquiries(self) -> List[Inquiry]:
        return list(self._inquiries)


inquiry_service = InquiryService()
