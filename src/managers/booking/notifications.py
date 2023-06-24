"""
Booking notification module for the Airport Management System.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class BookingNotifier:
    """Handles booking-related notifications."""
    
    def __init__(self):
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'your-email@gmail.com',  # Configure this
            'sender_password': 'your-app-password'   # Configure this
        }

    def send_booking_confirmation(self, email: str, booking_id: str, flight_details: dict) -> None:
        """Send booking confirmation email."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = email
            msg['Subject'] = f"Flight Booking Confirmation - {booking_id}"

            body = f"""
            Dear Passenger,

            Your flight has been successfully booked!

            Booking ID: {booking_id}
            Flight: {flight_details['flight_series']}{flight_details['flight_number']}
            From: {flight_details['departure']}
            To: {flight_details['arrival']}
            Departure: {flight_details['departure_time']}
            Arrival: {flight_details['arrival_time']}
            Seat: {flight_details['seat_number']}
            Price: ${flight_details['price']}

            Thank you for choosing our airline!

            Best regards,
            Airport Management System
            """

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['sender_email'], self.email_config['sender_password'])
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Error sending email: {e}") 