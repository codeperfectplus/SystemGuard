from flask import render_template, blueprints
from src.config import app
from src.models import SystemInformation

graphs_bp = blueprints.Blueprint("graphs", __name__)


@app.route('/graphs')
def graphs():
    # Query the last 3 entries from the SystemInformation table
    recent_system_info_entries = SystemInformation.query.all()
    
    if recent_system_info_entries:
        # Extract data from the query results
        time_data = [info.timestamp for info in recent_system_info_entries]
        cpu_data = [info.cpu_percent for info in recent_system_info_entries]
        memory_data = [info.memory_percent for info in recent_system_info_entries]
        battery_data = [info.battery_percent for info in recent_system_info_entries]
        network_sent_data = [info.network_sent for info in recent_system_info_entries]
        network_received_data = [info.network_received for info in recent_system_info_entries]

        # Print for debugging
        print("CPU Data:", cpu_data)
        print("Time Data:", time_data)

    # Pass the data to the template
    return render_template('graphs.html', cpu=cpu_data, time=time_data, 
                           memory=memory_data, battery=battery_data, 
                           network_sent=network_sent_data, 
                           network_received=network_received_data)
