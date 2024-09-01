import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

from src.config import app
from src.models import EmailPassword, DashboardSettings
# Load environment variables from .env file
load_dotenv()

# Get email credentials from .env
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(receiver_email, subject, body, attachment_path=None):
        
    if isinstance(receiver_email, str):
        receiver_email = [receiver_email]  # Convert single address to list

    with app.app_context():
        dasboard_settings = DashboardSettings.query.first()
        if dasboard_settings:
            enable_alerts = dasboard_settings.enable_alerts
            if not enable_alerts:
                print("Email alerts are disabled. Please enable them in the settings.")
                return {
                    "message": "Email alerts are disabled. Please enable them in the settings.",
                    "status": "failed",
                    "type": "general_settings",
                }
        email_password = EmailPassword.query.first()
        if not email_password:
            print("Email credentials not found. Please set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables.")
            return {
                "message": "Email credentials not found. Please set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables.",
                "status": "failed",
                "type": "update_email_password",
            }


    for email in receiver_email:
        try:
            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = email
            msg['Subject'] = subject
            # Append message to the body
            append_message = "This is an automated email from the SystemGuard application. Please do not reply to this email."
            full_body = body + "\n\n" + append_message

            # Attach the body with the msg instance
            msg.attach(MIMEText(full_body, 'plain'))

            # Attach a file if provided
            if attachment_path:
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {os.path.basename(attachment_path)}",
                    )
                    msg.attach(part)

            # Create an SMTP session
            with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Use Gmail's SMTP server
                server.starttls()  # Enable security

                # Login with sender's email and password
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

                # Send the email
                text = msg.as_string()
                server.sendmail(EMAIL_ADDRESS, email, text)

            return {
                "message": f"Email sent successfully to {email}",
                "status": "success",
            }

        except Exception as e:
            return {
                "message": f"failed to send email to {email}. Error: {str(e)}",
                "status": "failed",
            }

