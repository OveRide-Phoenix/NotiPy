import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set up GPIO
GPIO.setmode(GPIO.BCM)
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)

# Email setup
SMTP_SERVER = 'smtp.your-email-provider.com'
SMTP_PORT = 587
EMAIL = 'your-email@example.com'
PASSWORD = 'your-email-password'
TO_EMAIL = 'recipient-email@example.com'

def send_email():
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = "Motion Detected!"
    body = "Motion has been detected by your Raspberry Pi security system."
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL, TO_EMAIL, text)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

try:
    print("PIR Module Test (CTRL+C to exit)")
    time.sleep(2)
    print("Ready")

    while True:
        if GPIO.input(PIR_PIN):
            print("Motion Detected!")
            send_email()
            time.sleep(10)  # to prevent multiple emails for a single motion event
        time.sleep(1)
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
