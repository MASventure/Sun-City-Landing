from flask import Flask

from backend.routes import api_blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api_blueprint)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
