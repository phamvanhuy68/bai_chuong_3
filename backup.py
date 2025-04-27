import schedule
import time
import datetime
import os
import shutil
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
BACKUP_FOLDER = "backup_database"

def backup_database():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    success = True
    error_message = ""

    # Create backup folder if it doesn't exist
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    try:
        for filename in os.listdir("."):
            if filename.endswith(".sql") or filename.endswith(".sqlite3"):
                source_path = os.path.join(".", filename)
                destination_filename = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
                destination_path = os.path.join(BACKUP_FOLDER, destination_filename)
                shutil.copy2(source_path, destination_path)  # copy2 preserves metadata
        backup_status = "thành công"
    except Exception as e:
        success = False
        backup_status = "thất bại"
        error_message = str(e)

    send_notification_email(backup_status, error_message)

def send_notification_email(status, error=""):
    subject = f"Thông báo Backup Database ({status})"
    body = f"Quá trình backup database lúc {datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')} đã {status}."
    if error:
        body += f"\nLỗi: {error}"

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("Email thông báo đã được gửi.")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")

# Thời gian chạy backup 
schedule.every().day.at("18:15").do(backup_database)

print("chờ... đang chạy lịch")

while True:
    schedule.run_pending()
    time.sleep(60)