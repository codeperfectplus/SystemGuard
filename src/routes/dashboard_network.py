from flask import render_template, blueprints

from src.config import app
from src.routes.helper.common_helper import admin_required

network_bp = blueprints.Blueprint('network', __name__)

@app.route('/dashboard_network', methods=['GET'])
@admin_required
def dashboard_network():
    return render_template('network/dashboard_network.html')
