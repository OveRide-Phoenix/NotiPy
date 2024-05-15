# NotiPy: Raspberry Pi Home Security Device with Email Notifications

## Overview
NotiPy is a home security device that uses a Raspberry Pi and a PIR motion sensor to detect motion and send email notifications. This can be used to monitor your home or office space remotely.

## Components Needed
- Raspberry Pi (any model with internet connectivity)
- PIR Motion Sensor
- Resistors and Jumper Wires
- Breadboard
- Power Supply for Raspberry Pi
- MicroSD Card (with Raspbian OS installed)

## Software Requirements
- Raspbian OS
- Python 3
- smtplib (comes pre-installed with Python)

## Setup Instructions

### 1. Set Up the Raspberry Pi
1. Install Raspbian OS on the SD card.
2. Boot the Raspberry Pi and complete the initial configuration.
3. Update the system:
    ```sh
    sudo apt update
    sudo apt upgrade
    ```

### 2. Connect the PIR Motion Sensor
1. Connect the PIR sensor to the Raspberry Pi GPIO pins:
    - **VCC** to **5V**
    - **GND** to **GND**
    - **OUT** to **GPIO 17** (or any other GPIO pin you prefer)

### 3. Install Necessary Python Libraries
1. Install the RPi.GPIO library:
    ```sh
    sudo apt install python3-rpi.gpio
    ```

### 4. Write the Python Script
1. Create a new Python file (`motion_detector.py`) and paste the following code:

    ```python
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
    ```

### 5. Run the Script
1. Save the script and run it:
    ```sh
    python3 motion_detector.py
    ```

## Usage
- Ensure the Raspberry Pi and PIR sensor are properly connected and powered.
- Run the Python script to start monitoring for motion.
- When motion is detected, an email notification will be sent to the configured email address.

## Troubleshooting
- Verify the GPIO pin connections if the sensor is not detecting motion.
- Check the email credentials and SMTP server settings if emails are not being sent.
- Ensure your email provider allows less secure app access if you encounter login issues.

## Security Considerations
- Store email credentials securely and avoid hardcoding them directly in the script.
- Consider setting up a dedicated email account for this project.

## License
This project is open-source and available under the MIT License. Feel free to modify and distribute it as per the license terms.
