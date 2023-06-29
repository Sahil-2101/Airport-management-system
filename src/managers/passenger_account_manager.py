"""
Passenger account management module for the Airport Management System.
"""

from src.managers.passenger import (
    PassengerAuth, PassengerProfile, PassengerHistory, PassengerNotifier, PassengerBooking
)
from src.database.connection import DatabaseConnection
from datetime import datetime
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class PassengerAccountManager:
    """Handles all passenger account operations using modular components."""

    def __init__(self, db: DatabaseConnection, sender_email: str, sender_password: str):
        self.db = db
        self.auth = PassengerAuth(db)
        self.profile = PassengerProfile(db)
        self.history = PassengerHistory(db)
        self.notifier = PassengerNotifier(sender_email, sender_password)
        self.booking = PassengerBooking(db, self.notifier)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def _hash_password(self, password: str) -> str:
        """Hash the password for secure storage."""
        return hashlib.sha256(password.encode()).hexdigest()

    # Auth
    def login(self, username: str, password: str) -> bool:
        return self.auth.login(username, password)

    def change_password(self, username: str, current_password: str, new_password: str) -> bool:
        return self.auth.change_password(username, current_password, new_password)

    # Profile
    def create_account(self, username: str, password: str, email: str, name: str, phone: str) -> bool:
        hashed_password = self._hash_password(password)
        return self.profile.create_account(username, hashed_password, email, name, phone)

    def update_profile(self, username: str, field: str, new_value: str) -> bool:
        return self.profile.update_profile(username, field, new_value)

    def view_profile(self, username: str) -> None:
        self.profile.view_profile(username)

    # History
    def view_booking_history(self, username: str) -> None:
        self.history.view_booking_history(username)

    # Booking
    def book_flight(self, username: str, flight_series: str, flight_number: int, seat_number: str, payment_method: str) -> None:
        self.booking.book_flight(username, flight_series, flight_number, seat_number, payment_method)

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