from flask import jsonify, blueprints, request
from flask_login import login_required, current_user
from src.config import app, db
from src.models import SystemInformation, UserDashboardSettings
from src.utils import _get_system_info, get_os_release_info, get_os_info, get_cached_value
from datetime import datetime, timedelta
import gc

api_bp = blueprints.Blueprint("api", __name__)

@app.route("/api/system-info", methods=["GET"])
@login_required
def system_api():
    try:
        system_info = _get_system_info()
        return jsonify(system_info), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching the system information", "details": str(e)}), 500

@app.route('/api/v1/graphs_data', methods=['GET'])
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
            '1 month': timedelta(weeks=4)
        }
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
    