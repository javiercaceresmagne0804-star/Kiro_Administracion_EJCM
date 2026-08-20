from flask import Flask, jsonify

from db import db
from extensions import migrate
from academic.routes import academic_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("instance.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(academic_bp)

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.errorhandler(404)
    def not_found(_err):
        return jsonify(error="Recurso no encontrado"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
