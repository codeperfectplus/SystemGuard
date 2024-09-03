from src.config import db, app
from src.models.user_card_settings import UserCardSettings
from src.models.dashboard_netowrk import DashboardNetworkSettings
from src.models.user_dashboard_settings import UserDashboardSettings
from src.models.feature_toggle_settings import FeatureToggleSettings
from src.models.application_general_settings import ApplicationGeneralSettings
from src.models.smtp_configuration import SMTPSettings
from src.models.network_speed_test_result import NetworkSpeedTestResult
from src.models.system_information import SystemInformation
from src.models.user_profile import UserProfile
from flask_login import current_user
from werkzeug.security import generate_password_hash
import json



with app.app_context():
    print("Creating tables")
    db.create_all()

    # initialize default dashboard settings for users
    users = UserProfile.query.all()
    for user in users:
        if not user.dashboard_settings:
            db.session.add(UserDashboardSettings(user_id=user.id))
            db.session.add(UserCardSettings(user_id=user.id))
            db.session.add(FeatureToggleSettings(user_id=user.id))
            db.session.commit()

    pre_defined_users_json = "src/assets/predefine_user.json"
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

    # Initialize default settings
    general_settings = ApplicationGeneralSettings.query.first()
    if not general_settings:
        db.session.add(ApplicationGeneralSettings())
        db.session.commit()


# ibject for all templates
@app.context_processor
def inject_settings():
    if current_user.is_anonymous:
        return dict(settings=None, card_settings=None)
    general_settings = ApplicationGeneralSettings.query.first()
    card_settings = UserCardSettings.query.filter_by(user_id=current_user.id).first()
    settings = UserDashboardSettings.query.filter_by(
        user_id=current_user.id
    ).first()  # Retrieve user-specific settings from DB
    feature_toggles_settings = FeatureToggleSettings.query.filter_by(
        user_id=current_user.id
    ).first()
    all_settings = dict(
        settings=settings,
        general_settings=general_settings,
        card_settings=card_settings,
        feature_toggles_settings=feature_toggles_settings,
    )
    return all_settings
