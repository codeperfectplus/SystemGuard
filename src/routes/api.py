from flask import jsonify, blueprints, request
from flask_login import login_required, current_user
from src.config import app, db
from src.models import SystemInformation, UserDashboardSettings
from src.utils import _get_system_info

api_bp = blueprints.Blueprint("api", __name__)


@app.route("/api/system-info", methods=["GET"])
@login_required
def cpu_percent_api():
    try:
        system_info = _get_system_info()
        return jsonify(system_info), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching the system information", "details": str(e)}), 500


from flask import request
from datetime import datetime, timedelta

@app.route('/api/graphs_data')
@login_required
def graph_data_api():
    try:
        # Get the time filter from query parameters
        time_filter = request.args.get('filter', default='1 day')
        
        # Determine the start time based on the filter
        now = datetime.now()
        if time_filter == '1 day':
            start_time = now - timedelta(days=1)
        elif time_filter == '2 days':
            start_time = now - timedelta(days=2)
        elif time_filter == '3 days':
            start_time = now - timedelta(days=3)
        elif time_filter == '1 week':
            start_time = now - timedelta(weeks=1)
        elif time_filter == '1 month':
            start_time = now - timedelta(weeks=4)
        else:
            start_time = now - timedelta(days=1)  # Default to 1 day if filter is unknown


        # Fetch entries within the time range
        recent_system_info_entries = SystemInformation.query.filter(
            SystemInformation.timestamp >= start_time
        ).all()

        # Use list comprehension to extract data fields if entries exist, else provide empty lists
        if recent_system_info_entries:
            time_data, cpu_data, memory_data, battery_data, network_sent_data, network_received_data, \
            dashboard_memory_usage, cpu_frequency, current_temp = zip(*[
                (
                    info.timestamp, info.cpu_percent, info.memory_percent, info.battery_percent,
                    info.network_sent, info.network_received, info.dashboard_memory_usage,
                    info.cpu_frequency, info.current_temp
                )
                for info in recent_system_info_entries
            ])
        else:
            time_data = cpu_data = memory_data = battery_data = network_sent_data = network_received_data = []
            dashboard_memory_usage = cpu_frequency = current_temp = []
        # Return the data as JSON
        return jsonify({
            "time": time_data,
            "cpu": cpu_data,
            "memory": memory_data,
            "battery": battery_data,
            "network_sent": network_sent_data,
            "network_received": network_received_data,
            "dashboard_memory_usage": dashboard_memory_usage,
            "cpu_frequency": cpu_frequency,
            "current_temp": current_temp
        }), 200
    except Exception as e:
        # Handle and log the error for debugging purposes
        return jsonify({'error': 'An error occurred while fetching the graph data', 'details': str(e)}), 500

@app.route('/refresh-interval', methods=['GET', 'POST'])
@login_required
def manage_refresh_interval():
    try:
        # Get refresh interval (GET request)
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
