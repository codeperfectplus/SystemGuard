import requests
from datetime import datetime, timezone
from flask import jsonify, blueprints, request
from flask_login import login_required, current_user

from src.config import app, db
from src.models import UserDashboardSettings
from src.utils import _get_system_info, get_os_release_info, get_os_info, get_cached_value
from src.routes.helper.common_helper import admin_required
from src.routes.helper.prometheus_helper import (
    load_prometheus_config, 
    save_prometheus_config, 
    load_alert_rules, 
    save_alert_rules
)

api_bp = blueprints.Blueprint("api", __name__)

PROMETHEUS_BASE_URL = "http://localhost:9090"
QUERY_API_URL = f'{PROMETHEUS_BASE_URL}/api/v1/query_range'
TARGETS_API_URL = f'{PROMETHEUS_BASE_URL}/api/v1/targets'

PROMETHEUS_METRICS = {
    'cpu': 'cpu_usage_percentage',  # Adjusting to match the defined gauge
    'memory': 'memory_usage_percentage',
    'battery': 'battery_percentage',
    'network_sent': 'network_bytes_sent',
    'network_received': 'network_bytes_received',
    'dashboard_memory_usage': 'dashboard_memory_usage_percentage',
    'cpu_frequency': 'cpu_frequency',
    'current_temp': 'cpu_temperature',
}

@app.route("/api/v1/system-info", methods=["GET"])
@login_required
def system_api():
    try:
        system_info = _get_system_info()
        return jsonify(system_info), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching the system information", "details": str(e)}), 500

@app.route('/api/v1/prometheus/graphs_data', methods=['GET'])
@login_required
def graph_data_api():
    try:
        # Initialize lists for the data
        time_data = []
        metric_data = {}
        current_time = datetime.now()

        # Get the time filter from query parameters
        time_filter = request.args.get('filter', default='1 day')

        # Determine the start time based on the filter
        time_deltas = {
            '5 minutes': 5 * 60,
            '15 minutes': 15 * 60,
            '30 minutes': 30 * 60,
            '1 hour': 60 * 60,
            '3 hours': 3 * 60 * 60,
            '6 hours': 6 * 60 * 60,
            '12 hours': 12 * 60 * 60,
            '1 day': 24 * 60 * 60,
            '2 days': 2 * 24 * 60 * 60,
            '3 days': 3 * 24 * 60 * 60,
            '1 week': 7 * 24 * 60 * 60,
            '1 month': 30 * 24 * 60 * 60,
            '3 months': 90 * 24 * 60 * 60,
        }

        # Get the time range in seconds
        time_range_seconds = time_deltas.get(time_filter, 24 * 60 * 60)

        # Prepare time parameters for the Prometheus query
        end_time = int(current_time.timestamp())
        start_time = end_time - time_range_seconds

        # Determine the step based on the time range
        if time_range_seconds <= 900:  # 15 minutes
            step = '10s'
        elif time_range_seconds <= 3600:  # 1 hour
            step = '30s'
        elif time_range_seconds <= 86400:  # 1 day
            step = '1m'
        elif time_range_seconds <= 604800:  # 1 week
            step = '10m'
        else:  # More than 1 week
            step = '1h'
        
        # Fetch data for each metric from Prometheus
        for metric, prometheus_query in PROMETHEUS_METRICS.items():
            # Prepare Prometheus API query parameters
            params = {
                'query': prometheus_query,
                'start': start_time,
                'end': end_time,
                'step': step
            }

            # Send the query to Prometheus
            response = requests.get(QUERY_API_URL, params=params)
            
            # Check if the request was successful
            if response.status_code == 200:
                result = response.json().get('data', {}).get('result', [])
                
                if result:
                    # Initialize a dictionary to hold time series data for this metric
                    metric_data[metric] = []
                    
                    for series in result:
                        # Create a new list for the time series data of this particular series
                        series_data = {
                            "metric": series.get("metric"),
                            "values": {}
                        }
                        
                        # Iterate over the values for this series
                        for value in series.get("values", []):
                            timestamp = datetime.fromtimestamp(float(value[0]), tz=timezone.utc).isoformat()
                            if timestamp not in time_data:
                                time_data.append(timestamp)
                            series_data["values"][timestamp] = value[1]
                        
                        # Append the series data to the metric
                        metric_data[metric].append(series_data)
                else:
                    print(f"No data for metric: {metric}")
            else:
                raise Exception(f"Failed to fetch data for {metric} from Prometheus: {response.text}")

        # Sort the time data for proper alignment
        time_data.sort()

        # Ensure all metric data aligns with time_data
        for metric, series_list in metric_data.items():
            for series in series_list:
                aligned_values = []
                for timestamp in time_data:
                    aligned_values.append(series["values"].get(timestamp, None))
                series["values"] = aligned_values

        # Return the data as JSON
        response_data = {
            "time": time_data,
            **{metric: [{"metric": s["metric"], "values": s["values"]} for s in series_list] for metric, series_list in metric_data.items()},
            "current_time": current_time
        }

        return jsonify(response_data), 200

    except Exception as e:
        # Handle and log the error for debugging purposes
        return jsonify({'error': 'An error occurred while fetching the graph data', 'details': str(e)}), 500


@app.route('/api/v1/targets', methods=['GET'])
@admin_required
def get_prometheus_targets():
    try:
        # Query Prometheus API to get the targets
        response = requests.get(TARGETS_API_URL)
        
        # Check if the request was successful
        if response.status_code == 200:
            targets_data = response.json().get('data', {})
            active_targets = targets_data.get('activeTargets', [])
            dropped_targets = targets_data.get('droppedTargets', [])
            
            # Return the active and dropped targets as JSON
            return jsonify({
                'active_targets': active_targets,
                'dropped_targets': dropped_targets
            }), 200
        else:
            # Handle non-200 responses from Prometheus
            return jsonify({
                'error': 'Failed to fetch targets from Prometheus',
                'details': response.text
            }), response.status_code
    
    except Exception as e:
        # Handle exceptions
        return jsonify({
            'error': 'An error occurred while fetching Prometheus targets',
            'details': str(e)
        }), 500


@app.route('/api/v1/refresh-interval', methods=['GET', 'POST'])
@login_required
def manage_refresh_interval():
    try:
        if request.method == 'GET':
            settings = UserDashboardSettings.query.filter_by(user_id=current_user.id).first()
            if not settings:
                return jsonify({'refresh_interval': 30}), 200  # Default to 30 seconds
            return jsonify({
                "success": "Refresh interval fetched successfully",
                'refresh_interval': settings.refresh_interval
            }), 200

        # Update refresh interval (POST request)
        if request.method == 'POST':
            new_interval = request.json.get('refresh_interval')

            # Validate the new refresh interval
            if not isinstance(new_interval, int) or new_interval <= 0:
                return jsonify({'error': 'Invalid refresh interval value'}), 400

            # Find or create the user settings
            settings = UserDashboardSettings.query.filter_by(user_id=current_user.id).first()
            if not settings:
                settings = UserDashboardSettings(user_id=current_user.id, refresh_interval=new_interval)
                db.session.add(settings)
            else:
                settings.refresh_interval = new_interval

            db.session.commit()
            return jsonify({'success': 'Refresh interval updated successfully', 'refresh_interval': new_interval}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


@app.route('/api/v1/os-info', methods=['GET'])
@login_required
def get_os_info_api():
    os_info = get_cached_value("os_info", get_os_info)
    try:
        os_info.update(get_cached_value("os_release_info", get_os_release_info))
        return jsonify(os_info), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching the OS information", "details": str(e)}), 500


# Endpoint to view the current configuration
@app.route("/api/v1/prometheus/config", methods=["GET", "POST"])
def manage_prometheus_config():
    config = load_prometheus_config()
    if request.method == "POST":
        new_config = request.json
        config.update(new_config)
        save_prometheus_config(config)
        return jsonify({"message": "Configuration updated successfully"}), 200
    return jsonify(config)


# Endpoint to get the current alert rules
@app.route("/api/v1/prometheus/rules", methods=["GET", "POST"])
def manage_alert_rules():
    if request.method == "POST":
        new_rule = request.json
        rules = load_alert_rules()
        if "groups" not in rules:
            rules["groups"] = []
        rules["groups"].append(new_rule)
        save_alert_rules(rules)
        return jsonify({"message": "Alert rule added successfully"}), 200

    rules = load_alert_rules()
    return jsonify(rules)

# Reload Prometheus configuration
def reload_prometheus():
    url = f"{PROMETHEUS_BASE_URL}/-/reload"
    response = requests.post(url)
    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Prometheus configuration reloaded"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to reload Prometheus config", "details": response.text}), response.status_code

@app.route("/api/v1/prometheus/reload", methods=["POST"])
def reload_prometheus_config():
    return reload_prometheus()


@app.route("/api/v1/prometheus/ready")
def ready_prometheus():
    url = f"{PROMETHEUS_BASE_URL}/-/ready"
    response = requests.get(url)

    if response.status_code == 200:
        return jsonify({"status": "success", "message": response.text}), 200
    else:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Prometheus is not ready.",
                    "details": response.text,
                }
            ),
            response.status_code,
        )
