import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def format_alert_message(alert_data):
    server_info = alert_data['server_info']
    anomalies = alert_data['anomalies']
    timestamp = alert_data['timestamp']
    
    message = f"""
ALERT: System Anomalies Detected

Server Information:
- Hostname: {server_info['hostname']}
- IP Address: {server_info['ip']}
- Operating System: {server_info['os']}
- Time: {timestamp}

Anomalies Detected:
"""
    
    for metric, value in anomalies.items():
        message += f"- {metric.upper()}: {value}%\n"
    
    return message

def send_alert(alert_data):
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')

    if not all([email_user, email_password]):
        print("Warning: Email credentials not configured. Skipping alert.")
        return

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            try:
                server.login(email_user, email_password)
            except smtplib.SMTPAuthenticationError:
                print("\nEmail Authentication Error!")
                print("Please make sure you've set up the App Password correctly:")
                print("1. Go to https://myaccount.google.com/security")
                print("2. Scroll down to 'App passwords'")
                print("3. Generate a new App Password")
                print("4. Update the EMAIL_PASSWORD in your .env file")
                return
            
            msg = MIMEMultipart()
            msg['Subject'] = f"System Alert: Anomalies on {alert_data['server_info']['hostname']}"
            msg['From'] = email_user
            msg['To'] = email_user
            
            body = format_alert_message(alert_data)
            msg.attach(MIMEText(body, 'plain'))
            
            server.send_message(msg)
            print(f"Alert sent successfully for server {alert_data['server_info']['hostname']}")
    except Exception as e:
        print(f"Failed to send alert: {str(e)}") 