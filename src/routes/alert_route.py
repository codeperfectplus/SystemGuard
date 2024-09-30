import os
from flask import request, jsonify, Blueprint
from src.config import app
from src.logger import logger

from src.routes.helper.notification_helper import send_test_alert, process_alert
from src.utils import get_ip_address

alert_bp = Blueprint("alert", __name__)

@app.route("/alerts", methods=["POST"])
def receive_alerts():
    """
    Receives and processes incoming alerts from external sources.

    Validates the request content type and alert data, logs the alert based on severity,
    and triggers notifications via Slack, email, and Discord.

    Returns:
        JSON response indicating the result of alert processing:
        - 200 if successfully processed
        - 400 if alert data is missing
        - 415 if the content type is not application/json
        - 500 if an internal server error occurs
    """
    if request.headers.get("Content-Type") != "application/json":
        return (
            jsonify({"error": "Unsupported Media Type. Expected application/json"}),
            415,
        )

    try:
        alert_data = request.json
        if not alert_data or "alerts" not in alert_data:
            return jsonify({"error": "No alert data received"}), 400

        for alert in alert_data["alerts"]:
            process_alert(alert)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.exception("Error occurred while processing alert")
        return (
            jsonify({"error": "An internal error occurred while processing the alert"}),
            500,
        )


@app.route("/alerts/test", methods=["GET"])
def test_alert():
    alertmanager_ip = get_ip_address()
    alertmanager_port = "9093"
    alertmanager_url = f"http://{alertmanager_ip}:{alertmanager_port}"

    # Send a test alert with a unique name
    response = send_test_alert(alertmanager_url, "Test Alert", "info", "Test Instance")
    return jsonify(response), response.get("status", 500)
