from flask import Blueprint

from backend.routes import amenities, inquiries

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api_blueprint.register_blueprint(amenities.blueprint)
api_blueprint.register_blueprint(inquiries.blueprint)

__all__ = ["api_blueprint"]
