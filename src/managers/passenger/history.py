"""
Booking history management for passenger accounts.
"""

class PassengerHistory:
    def __init__(self, db):
        self.db = db

    def view_booking_history(self, username: str) -> None:
        """Display passenger's booking history."""
        query = """
            SELECT f.flightseries, f.flightnumber, f.departure, f.arrival,
                   f.departuretime, f.arrivaltime, f.status
            FROM passenger_accounts pa
            JOIN passenger p ON pa.name = p.name
            JOIN flight f ON p.flightserial = f.flightseries 
            AND p.flightnumber = f.flightnumber
            WHERE pa.username = %s
            ORDER BY f.departuretime DESC
        """
        result = self.db.execute_query(query, (username,))
        if result:
            print("\nBooking History:")
            print("Flight\tFrom\tTo\tDeparture\tArrival\tStatus")
            for row in result:
                print(f"{row[0]}{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}")
        else:
            print("No booking history found") 