from flask import Blueprint, Response
from prometheus_client import generate_latest
from src.config import app

# Define the Prometheus Blueprint
prometheus_bp = Blueprint('prometheus', __name__)

# Define a route to serve Prometheus metrics
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')
