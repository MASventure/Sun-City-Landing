from flask import Blueprint, jsonify, request

from backend.models.inquiry import Inquiry
from backend.services.inquiry_service import inquiry_service

blueprint = Blueprint("inquiries", __name__)


def _validate_payload(payload: dict) -> tuple[bool, str | None]:
    required_fields = ["name", "email", "phone", "preferred_date"]

    for field in required_fields:
        if not payload.get(field):
            return False, f"Missing required field: {field}"
    return True, None


@blueprint.post("/inquiries")
def create_inquiry():
    payload = request.get_json(silent=True) or {}

    is_valid, error_message = _validate_payload(payload)
    if not is_valid:
        return jsonify({"message": error_message}), 400

    inquiry = Inquiry(
        name=payload["name"],
        email=payload["email"],
        phone=payload["phone"],
        preferred_date=payload["preferred_date"],
        message=payload.get("message"),
    )
    inquiry_service.add_inquiry(inquiry)

    return jsonify({"message": "Inquiry received", "inquiry": inquiry.to_dict()}), 201


@blueprint.get("/inquiries")
def list_inquiries():
    data = [inquiry.to_dict() for inquiry in inquiry_service.list_inquiries()]
    return jsonify({"inquiries": data})
