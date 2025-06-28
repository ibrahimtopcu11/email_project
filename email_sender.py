import smtplib
import yaml
import os
from email.message import EmailMessage
from users import Users

def load_config():
    with open("conf.yaml", "r") as f:
        return yaml.safe_load(f)

def send_email(to_email, subject, message, config, password):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = config["server_email"]
    msg["To"] = to_email
    msg.set_content(message)

    with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
        server.starttls()
        server.login(config["server_email"], password)
        server.send_message(msg)

if __name__ == "__main__":
    who = os.environ.get("WHO", "").strip().lower()
    if who not in Users:
        raise ValueError("User not found in Users dictionary.")

    message = os.environ.get("MESSAGE", f"Hello {who.capitalize()}")
    config = load_config()
    to_email = Users[who]
    password = os.environ["EMAIL_PASSWORD"]  

    send_email(to_email, "Automated Message", message, config, password)
