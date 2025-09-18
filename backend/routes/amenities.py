from flask import Blueprint, jsonify

from backend.data.amenities import AMENITIES

blueprint = Blueprint("amenities", __name__)


@blueprint.get("/amenities")
def list_amenities():
    """Return the set of amenities promoted on the landing page."""

    return jsonify({"amenities": AMENITIES})
