from flask import render_template, request, blueprints

from src.config import app
from src.routes.helper.network_helper import handle_network_scan, handle_port_scan

experimental_bp = blueprints.Blueprint('experimental', __name__)

@app.route('/security_analysis', methods=['GET', 'POST'])
def security_analysis():
    if request.method == 'POST':
        if 'scan_network' in request.form:
            return handle_network_scan()
        elif 'scan_ports' in request.form:
            return handle_port_scan()
    
    # Render the default scan page if the request method is GET or no valid action is found in POST.
    return render_template('experimental/scan.html')

