"""
Notification management for passenger accounts.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class PassengerNotifier:
    def __init__(self, sender_email, sender_password, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_confirmation_email(self, recipient_email: str, booking_details: str) -> None:
        """Send a confirmation email for booking."""
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Booking Confirmation"
        body = f"Thank you for your booking. Here are your booking details:\n{booking_details}"
        msg.attach(MIMEText(body, 'plain'))
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            print("Confirmation email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}") 