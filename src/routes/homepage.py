from flask import render_template, blueprints, flash, redirect, url_for, request
from flask_login import login_required, current_user

from src.config import app, db
from src.utils import get_cached_value, get_memory_percent, get_memory_available, get_memory_used, get_swap_memory_info
from src.models import  DashboardNetworkSettings

homepages_bp = blueprints.Blueprint('homepages', __name__)


from flask import render_template
from flask_login import login_required

@app.route('/', methods=['GET'])
@login_required
def dashboard_network():
    groups = DashboardNetworkSettings.query.all()  # Fetch all dashboard groups
    return render_template('dashboard_network.html', groups=groups)


@app.route('/add_server', methods=['GET', 'POST'])
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

    return render_template('add_server.html')

@app.route('/edit_server/<int:server_id>', methods=['GET', 'POST'])
@login_required
def edit_server(server_id):
    if current_user.user_level != 'admin':
        flash('You are not authorized to access this page.', 'danger')
        return render_template("error/permission_denied.html")

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
    return render_template('edit_server.html', server=server)

@app.route('/delete_server/<int:server_id>', methods=['POST'])
@login_required
def delete_server(server_id):
    if current_user.user_level != 'admin':
        flash('You are not authorized to access this page.', 'danger')
        return render_template("error/permission_denied.html")
    server = DashboardNetworkSettings.query.get_or_404(server_id)
    db.session.delete(server)
    db.session.commit()
    flash('Server deleted successfully!', 'success')
    return redirect(url_for('dashboard_network'))
