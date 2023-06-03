"""
Booking management module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection
from datetime import datetime
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class BookingManager:
    """Handles all flight booking operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'your-email@gmail.com',  # Configure this
            'sender_password': 'your-app-password'   # Configure this
        }

    def _generate_booking_id(self) -> str:
        """Generate a unique booking ID."""
        return str(uuid.uuid4())[:8].upper()

    def _send_booking_confirmation(self, email: str, booking_id: str, flight_details: dict) -> None:
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

    def get_available_seats(self, flight_series: str, flight_number: int) -> list:
        """Get list of available seats for a flight."""
        query = """
            SELECT seat_number 
            FROM seats 
            WHERE flight_series = %s 
            AND flight_number = %s 
            AND is_available = TRUE
        """
        result = self.db.execute_query(query, (flight_series, flight_number))
        return [row[0] for row in result] if result else []

    def book_flight(self, username: str, flight_series: str, flight_number: int, 
                   seat_number: str, payment_method: str) -> bool:
        """Book a flight for a passenger."""
        try:
            # Get passenger details
            query = "SELECT email, name FROM passenger_accounts WHERE username = %s"
            passenger = self.db.execute_query(query, (username,))
            if not passenger:
                print("Passenger account not found")
                return False

            # Get flight details
            query = """
                SELECT departure, arrival, departuretime, arrivaltime, price 
                FROM flight 
                WHERE flightseries = %s AND flightnumber = %s
            """
            flight = self.db.execute_query(query, (flight_series, flight_number))
            if not flight:
                print("Flight not found")
                return False

            # Check seat availability
            if not self.get_available_seats(flight_series, flight_number):
                print("No seats available")
                return False

            # Generate booking ID
            booking_id = self._generate_booking_id()

            # Create booking record
            query = """
                INSERT INTO bookings (
                    booking_id, username, flight_series, flight_number,
                    seat_number, booking_date, payment_method, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                booking_id, username, flight_series, flight_number,
                seat_number, datetime.now(), payment_method, 'CONFIRMED'
            )
            self.db.execute_query(query, params)

            # Update seat availability
            query = """
                UPDATE seats 
                SET is_available = FALSE 
                WHERE flight_series = %s 
                AND flight_number = %s 
                AND seat_number = %s
            """
            self.db.execute_query(query, (flight_series, flight_number, seat_number))

            # Update flight available seats
            query = """
                UPDATE flight 
                SET available = available - 1 
                WHERE flightseries = %s 
                AND flightnumber = %s
            """
            self.db.execute_query(query, (flight_series, flight_number))

            # Send confirmation email
            flight_details = {
                'flight_series': flight_series,
                'flight_number': flight_number,
                'departure': flight[0][0],
                'arrival': flight[0][1],
                'departure_time': flight[0][2],
                'arrival_time': flight[0][3],
                'seat_number': seat_number,
                'price': flight[0][4]
            }
            self._send_booking_confirmation(passenger[0][0], booking_id, flight_details)

            print(f"Booking confirmed! Your booking ID is: {booking_id}")
            return True

        except Exception as e:
            print(f"Error booking flight: {e}")
            return False

    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel a flight booking."""
        try:
            # Get booking details
            query = """
                SELECT flight_series, flight_number, seat_number, username 
                FROM bookings 
                WHERE booking_id = %s AND status = 'CONFIRMED'
            """
            booking = self.db.execute_query(query, (booking_id,))
            if not booking:
                print("Booking not found or already cancelled")
                return False

            # Update booking status
            query = "UPDATE bookings SET status = 'CANCELLED' WHERE booking_id = %s"
            self.db.execute_query(query, (booking_id,))

            # Update seat availability
            query = """
                UPDATE seats 
                SET is_available = TRUE 
                WHERE flight_series = %s 
                AND flight_number = %s 
                AND seat_number = %s
            """
            self.db.execute_query(query, (booking[0][0], booking[0][1], booking[0][2]))

            # Update flight available seats
            query = """
                UPDATE flight 
                SET available = available + 1 
                WHERE flightseries = %s 
                AND flightnumber = %s
            """
            self.db.execute_query(query, (booking[0][0], booking[0][1]))

            print("Booking cancelled successfully")
            return True

        except Exception as e:
            print(f"Error cancelling booking: {e}")
            return False

    def view_booking(self, booking_id: str) -> None:
        """View booking details."""
        query = """
            SELECT b.*, f.departure, f.arrival, f.departuretime, f.arrivaltime, f.price,
                   pa.email, pa.name
            FROM bookings b
            JOIN flight f ON b.flight_series = f.flightseries 
            AND b.flight_number = f.flightnumber
            JOIN passenger_accounts pa ON b.username = pa.username
            WHERE b.booking_id = %s
        """
        result = self.db.execute_query(query, (booking_id,))
        
        if result:
            print("\nBooking Details:")
            print(f"Booking ID: {result[0][0]}")
            print(f"Passenger: {result[0][7]} ({result[0][6]})")
            print(f"Flight: {result[0][2]}{result[0][3]}")
            print(f"From: {result[0][8]}")
            print(f"To: {result[0][9]}")
            print(f"Departure: {result[0][10]}")
            print(f"Arrival: {result[0][11]}")
            print(f"Seat: {result[0][4]}")
            print(f"Price: ${result[0][12]}")
            print(f"Status: {result[0][7]}")
            print(f"Booking Date: {result[0][5]}")
        else:
            print("Booking not found") 