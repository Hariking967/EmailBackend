from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

# Your Gmail credentials
SENDER_EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def send_email(to_email, subject, body, from_email=SENDER_EMAIL):
    try:
        # Create message
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Connect to Gmail SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(message)
        server.quit()

        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)


@app.route("/send-email", methods=["POST"])
def send_email_api():
    data = request.get_json()

    to_email = data.get("to")
    subject = data.get("subject")
    body = data.get("body")
    from_email = data.get("from", SENDER_EMAIL)  # optional override

    if not to_email or not subject or not body:
        return jsonify({"error": "Missing required fields"}), 400

    success, msg = send_email(to_email, subject, body, from_email)
    if success:
        return jsonify({"message": msg}), 200
    else:
        return jsonify({"error": msg}), 500


if __name__ == "__main__":
    app.run(debug=True)
