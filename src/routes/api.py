from flask import jsonify, blueprints, request
import requests
from flask_login import login_required, current_user
from src.config import app, db
from src.models import SystemInformation, UserDashboardSettings
from src.utils import _get_system_info, get_os_release_info, get_os_info, get_cached_value
from datetime import datetime, timedelta
from flask import request, jsonify
import gc
from datetime import datetime, timezone

from src.routes.helper.common_helper import admin_required

api_bp = blueprints.Blueprint("api", __name__)

PROMETHEUS_URL = 'http://localhost:9090'  # Change if using a different URL or port
QUERY_API_URL = f'{PROMETHEUS_URL}/api/v1/query'
TARGETS_API_URL = f'{PROMETHEUS_URL}/api/v1/targets'

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

@app.route("/api/system-info", methods=["GET"])
@login_required
def system_api():
    try:
        system_info = _get_system_info()
        return jsonify(system_info), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching the system information", "details": str(e)}), 500

@app.route('/api/v1/sqlite/graphs_data', methods=['GET'])
@login_required
def graph_data_api():
    try:
        current_time = datetime.now()
        # Get the time filter from query parameters
        time_filter = request.args.get('filter', default='1 day')

        # Determine the start time based on the filter
        now = datetime.now()
        time_deltas = {
            '5 minutes': timedelta(minutes=5),
            '15 minutes': timedelta(minutes=15),
            '30 minutes': timedelta(minutes=30),
            '1 hour': timedelta(hours=1),
            '3 hours': timedelta(hours=3),
            '6 hours': timedelta(hours=6),
            '12 hours': timedelta(hours=12),
            '1 day': timedelta(days=1),
            '2 days': timedelta(days=2),
            '3 days': timedelta(days=3),
            '1 week': timedelta(weeks=1),
            '1 month': timedelta(weeks=4),
            '3 months': timedelta(weeks=12),

        }
        if time_filter == 'all':
            start_time = datetime.min
        else:
            start_time = now - time_deltas.get(time_filter, timedelta(days=1))

        # Fetch entries within the time range
        query = SystemInformation.query.filter(SystemInformation.timestamp >= start_time)
        recent_system_info_entries = query.all()

        # Initialize lists for the data
        time_data = []
        cpu_data = []
        memory_data = []
        battery_data = []
        network_sent_data = []
        network_received_data = []
        dashboard_memory_usage = []
        cpu_frequency = []
        current_temp = []

        # Extract data fields if entries exist
        if recent_system_info_entries:
            for info in recent_system_info_entries:
                time_data.append(info.timestamp)
                cpu_data.append(info.cpu_percent)
                memory_data.append(info.memory_percent)
                battery_data.append(info.battery_percent)
                network_sent_data.append(info.network_sent)
                network_received_data.append(info.network_received)
                dashboard_memory_usage.append(info.dashboard_memory_usage)
                cpu_frequency.append(info.cpu_frequency)
                current_temp.append(info.current_temp)

        # Return the data as JSON
        response = jsonify({
            "time": time_data,
            "cpu": cpu_data,
            "memory": memory_data,
            "battery": battery_data,
            "network_sent": network_sent_data,
            "network_received": network_received_data,
            "dashboard_memory_usage": dashboard_memory_usage,
            "cpu_frequency": cpu_frequency,
            "current_temp": current_temp,
            "current_time": current_time
        })

        print("response", {
            "time": time_data,
            "cpu": cpu_data,
            "memory": memory_data,
            "battery": battery_data,    
            "network_sent": network_sent_data,
            "network_received": network_received_data,
            "dashboard_memory_usage": dashboard_memory_usage,
            "cpu_frequency": cpu_frequency,
            "current_temp": current_temp,
            "current_time": current_time
        })

        # Clean up large data structures
        del recent_system_info_entries
        del time_data
        del cpu_data
        del memory_data
        del battery_data
        del network_sent_data
        del network_received_data
        del dashboard_memory_usage
        del cpu_frequency
        del current_temp

        gc.collect()

        return response, 200
    except Exception as e:
        # Handle and log the error for debugging purposes
        return jsonify({'error': 'An error occurred while fetching the graph data', 'details': str(e)}), 500

# @app.route('/api/v2/influxdb/graphs_data', methods=['GET'])
# @login_required
# def graph_data_api_v2():
#     try:
#         current_time = datetime.now()
#         # Get the time filter from query parameters
#         time_filter = request.args.get('filter', default='1 day')

#         # Determine the start time based on the filter
#         time_deltas = {
#             '5 minutes': '-5m',
#             '15 minutes': '-15m',
#             '30 minutes': '-30m',
#             '1 hour': '-1h',
#             '3 hours': '-3h',
#             '6 hours': '-6h',
#             '12 hours': '-12h',
#             '1 day': '-1d',
#             '2 days': '-2d',
#             '3 days': '-3d',
#             '1 week': '-1w',
#             '1 month': '-30d',
#             '3 months': '-90d',
#         }

#         # Get the start time for the query
#         time_range = time_deltas.get(time_filter, '-1d')

#         # Build the InfluxDB query
#         flux_query = f"""
#         from(bucket: "{bucket}")
#         |> range(start: {time_range})
#         |> filter(fn: (r) => r._measurement == "system_info")
#         |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
#         """

#         # Execute the query
#         tables = query_api.query(flux_query)

#         # Initialize lists for the data
#         time_data = []
#         cpu_data = []
#         memory_data = []
#         battery_data = []
#         network_sent_data = []
#         network_received_data = []
#         dashboard_memory_usage = []
#         cpu_frequency = []
#         current_temp = []

#         # Parse the results
#         for table in tables:
#             for record in table.records:
#                 time_data.append(record.values.get("_time", None))
#                 # Extract each field by key (handle missing fields gracefully)
#                 cpu_data.append(record.values.get("cpu_percent", None))
#                 memory_data.append(record.values.get("memory_percent", None))
#                 battery_data.append(record.values.get("battery_percent", None))
#                 network_sent_data.append(record.values.get("network_sent", None))
#                 network_received_data.append(record.values.get("network_received", None))
#                 dashboard_memory_usage.append(record.values.get("dashboard_memory_usage", None))
#                 cpu_frequency.append(record.values.get("cpu_frequency", None))
#                 current_temp.append(record.values.get("current_temp", None))

#         # Return the data as JSON
#         response = jsonify({
#             "time": time_data,
#             "cpu": cpu_data,
#             "memory": memory_data,
#             "battery": battery_data,
#             "network_sent": network_sent_data,
#             "network_received": network_received_data,
#             "dashboard_memory_usage": dashboard_memory_usage,
#             "cpu_frequency": cpu_frequency,
#             "current_temp": current_temp,
#             "current_time": current_time
#         })

#         # Clean up large data structures
#         del tables
#         del time_data
#         del cpu_data
#         del memory_data
#         del battery_data
#         del network_sent_data
#         del network_received_data
#         del dashboard_memory_usage
#         del cpu_frequency
#         del current_temp

#         gc.collect()

#         return response, 200

#     except Exception as e:
#         # Handle and log the error for debugging purposes
#         return jsonify({'error': 'An error occurred while fetching the graph data', 'details': str(e)}), 500

@app.route('/api/v1/prometheus/graphs_data', methods=['GET'])
@login_required
def graph_data_api_v3():
    try:
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
        step = '10s'

        # Initialize lists for the data
        time_data = []
        metric_data = {key: [] for key in PROMETHEUS_METRICS}

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

                # Extract the time and values for the metric
                if result:
                    for value in result[0]['values']:
                        timestamp = datetime.fromtimestamp(float(value[0]), tz=timezone.utc).isoformat()
                        if timestamp not in time_data:
                            time_data.append(timestamp)
                        metric_data[metric].append(value[1])
                else:
                    print(f"No data for metric: {metric}")
            else:
                raise Exception(f"Failed to fetch data for {metric} from Prometheus: {response.text}")

        # Ensure all metric data has the same length as time_data
        for metric in metric_data:
            while len(metric_data[metric]) < len(time_data):
                metric_data[metric].append(None)

        # Return the data as JSON
        response_data = {
            "time": time_data,
            **metric_data,
            "current_time": current_time
        }

        return jsonify(response_data), 200

    except Exception as e:
        # Handle and log the error for debugging purposes
        return jsonify({'error': 'An error occurred while fetching the graph data', 'details': str(e)}), 500

@app.route('/api/v1/prometheus/graphs_data/targets', methods=['GET'])
@login_required
def graph_data_api_v3_():
    try:
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
        step = '10s'

        # Initialize lists for the data
        time_data = []
        metric_data = {}

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
    