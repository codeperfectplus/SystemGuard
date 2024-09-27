from flask import request, jsonify, blueprints
from src.config import app
from src.logger import logger

alert_bp = blueprints.Blueprint('alert', __name__)

@app.route('/alerts', methods=['POST'])
def receive_alerts():
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type: Expected application/json"}), 415
    
    try:
        print("Received alert:", request.json)
        alert_data = request.json
        if not alert_data:
            return jsonify({"error": "No data received"}), 400

        # Log or process the alerts as needed
        for alert in alert_data['alerts']:
            alert_name = alert['labels'].get('alertname')
            instance = alert['labels'].get('instance')
            severity = alert['labels'].get('severity')
            description = alert['annotations'].get('description')
            summary = alert['annotations'].get('summary')

            print(f"Alert received: {alert_name} - {instance} - {severity} - {description} - {summary}")

            logger.info(f"Alert received: {alert_name} - {instance} - {severity} - {description} - {summary}")

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
