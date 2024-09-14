from flask import render_template, blueprints, flash, redirect, url_for, request
from flask_login import login_required, current_user

from src.config import app, db
from src.models import  DashboardNetworkSettings
from src.routes.helper.common_helper import admin_required

network_bp = blueprints.Blueprint('network', __name__)


from flask import render_template
from flask_login import login_required

@app.route('/network', methods=['GET'])
@admin_required
def dashboard_network():
    groups = DashboardNetworkSettings.query.all()  # Fetch all dashboard groups
    return render_template('network/dashboard_network.html', groups=groups)


@app.route('/add_server', methods=['GET', 'POST'])
@admin_required
def add_server():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        ip_address = request.form.get('ip_address')
        port = request.form.get('port')
        link = request.form.get('link')

        # Check if the server name already exists
        existing_server = DashboardNetworkSettings.query.filter_by(name=name).first()
        if existing_server:
            flash('Server name already exists. Please choose a different name.', 'danger')
            return redirect(url_for('add_server'))

        # Create a new server entry
        new_server = DashboardNetworkSettings(name=name, description=description, ip_address=ip_address, port=port, link=link)
        db.session.add(new_server)
        db.session.commit()

        flash('Server added successfully!', 'success')
        return redirect(url_for('dashboard_network'))

    return render_template('network/add_server.html')

@app.route('/edit_server/<int:server_id>', methods=['GET', 'POST'])
@admin_required
def edit_server(server_id):
    server = DashboardNetworkSettings.query.get_or_404(server_id)
    if request.method == 'POST':
        server.name = request.form['name']
        server.description = request.form['description']
        server.ip_address = request.form['ip_address']
        server.port = request.form['port']
        server.link = request.form['link']
        db.session.commit()
        flash('Server updated successfully!', 'success')
        return redirect(url_for('dashboard_network'))
    return render_template('network/edit_server.html', server=server)

@app.route('/delete_server/<int:server_id>', methods=['POST'])
@admin_required
def delete_server(server_id):
    server = DashboardNetworkSettings.query.get_or_404(server_id)
    db.session.delete(server)
    db.session.commit()
    flash('Server deleted successfully!', 'success')
    return redirect(url_for('dashboard_network'))
