from flask import jsonify, blueprints
from src.config import app

health_bp = blueprints.Blueprint("health", __name__)

# health page
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

