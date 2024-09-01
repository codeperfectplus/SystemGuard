import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get email credentials from .env
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(receiver_email, subject, body, attachment_path=None):
    try:
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiver_email
        msg['Subject'] = subject
        # append message to the body
        append_message = "This is an automated email from the SystemGuru application. Please do not reply to this email."
        body = body + "\n\n" + append_message

        # Attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # Attach a file if provided
        if attachment_path:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {attachment_path}",
                )
                msg.attach(part)

        # Create an SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use Gmail's SMTP server
        server.starttls()  # Enable security

        # Login with sender's email and password
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Send the email
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, receiver_email, text)

        # Close the SMTP session
        server.quit()

        print(f"Email sent successfully to {receiver_email}")

    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
