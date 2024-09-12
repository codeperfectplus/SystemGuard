from src.config import db, app
from src.models.user_card_settings import UserCardSettings
from src.models.dashboard_netowrk import DashboardNetworkSettings
from src.models.user_dashboard_settings import UserDashboardSettings
from src.models.page_toggle_settings import PageToggleSettings
from src.models.application_general_settings import GeneralSettings
from src.models.smtp_configuration import SMTPSettings
from src.models.network_speed_test_result import NetworkSpeedTestResult
from src.models.system_information import SystemInformation
from src.models.user_profile import UserProfile
from src.models.monitored_website import MonitoredWebsite
from flask_login import current_user
from src.logger import logger
from werkzeug.security import generate_password_hash
import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with app.app_context():
    logger.info("Creating tables")
    db.create_all()

    # initialize default dashboard user_dashboard_settings for users
    users = UserProfile.query.all()
    for user in users:
        if not user.dashboard_settings:
            db.session.add(UserDashboardSettings(user_id=user.id))
            db.session.add(UserCardSettings(user_id=user.id))
            db.session.add(PageToggleSettings(user_id=user.id))
            
            db.session.commit()
            logger.info("Initial card data added.")
            db.session.commit()

    pre_defined_users_json = os.path.join(ROOT_DIR, "src/assets/predefine_user.json")
    with open(pre_defined_users_json, "r") as file:
        pre_defined_users = json.load(file)
    for user in pre_defined_users:
        if not UserProfile.query.filter_by(user_level=user["user_level"]).first():
            hashed_password = generate_password_hash(user["password"])
            user = UserProfile(
                username=user["username"],
                email=user["email"],
                password=hashed_password,
                user_level=user["user_level"],
                receive_email_alerts=user["receive_email_alerts"],
                profession=user["profession"],
            )

            db.session.add(user)
            db.session.commit()

    # Initialize default user_dashboard_settings
    general_settings = GeneralSettings.query.first()
    if not general_settings:
        db.session.add(GeneralSettings())
        db.session.commit()


# ibject for all templates
@app.context_processor
def inject_settings():
    if current_user.is_anonymous:
        user_dashboard_settings = UserDashboardSettings(user_id=0)
        card_settings = None
        page_toggles_settings = None
        general_settings = None
        return dict(
            user_dashboard_settings=user_dashboard_settings,
            card_settings=card_settings,
            page_toggles_settings=page_toggles_settings,
            general_settings=general_settings,
        )
    general_settings = GeneralSettings.query.first()
    card_settings = UserCardSettings.query.filter_by(user_id=current_user.id).first()
    user_dashboard_settings = UserDashboardSettings.query.filter_by(
        user_id=current_user.id
    ).first()  # Retrieve user-specific user_dashboard_settings from DB
    page_toggles_settings = PageToggleSettings.query.filter_by(
        user_id=current_user.id
    ).first()
    all_settings = dict(
        user_dashboard_settings=user_dashboard_settings,
        general_settings=general_settings,
        card_settings=card_settings,
        page_toggles_settings=page_toggles_settings,
    )
    return all_settings
