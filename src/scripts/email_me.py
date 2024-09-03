import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import redirect, url_for, flash
from src.config import app
from src.models import ApplicationGeneralSettings, SMTPSettings

system_name = os.uname().sysname

def send_smpt_email(receiver_email, subject, body, attachment_path=None, is_html=False, bypass_alerts=False):
        
    if isinstance(receiver_email, str):
        receiver_email = [receiver_email]  # Convert single address to list

    with app.app_context():
        if not bypass_alerts:
            general_settings = ApplicationGeneralSettings.query.first()
            if general_settings:
                enable_alerts = general_settings.enable_alerts
                if not enable_alerts:
                    print("Email alerts are disabled. Please enable them in the settings.")
                    flash("Email alerts are disabled. Please enable them in the settings.", "danger")
                    return redirect(url_for('general_settings'))
    
        email_password = SMTPSettings.query.first()
        if not email_password:
            print("SMTP email credentials not found. Please set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables.")
            flash("SMTP email credentials not found. Please set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables.", "danger")
            return redirect(url_for('update_smpt_email_password'))

    EMAIL_ADDRESS = email_password.email
    EMAIL_PASSWORD = email_password.password

    print(f"Sending email to {receiver_email}")

    for email in receiver_email:
        try:
            server_name = os.uname().nodename
            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = email
            msg['Subject'] = "SystemGuard Alert from " + system_name + " (" + server_name + "): " + subject
            # Append message to the body
            append_message = "This is an automated email from the SystemGuard application. Please do not reply to this email."
            
            if is_html:
                # If the email is HTML, append the message in HTML format
                full_body = body + f"<p>{append_message}</p>"
                msg.attach(MIMEText(full_body, 'html'))
            else:
                # If the email is plain text, append the message in plain text format
                full_body = body + "\n\n" + append_message
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
            print(f"Failed to send email to {email}. Error: {str(e)}")
            return {
                "message": f"Failed to send email to {email}. Error: {str(e)}",
                "status": "failed",
            }
