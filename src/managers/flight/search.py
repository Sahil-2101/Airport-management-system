"""
Flight search module for the Airport Management System.
"""

from src.database.connection import DatabaseConnection

class FlightSearch:
    """Handles flight search operations."""
    
    def __init__(self):
        """Initialize the flight search manager."""
        self.db = DatabaseConnection()
        self.last_searched_route = None

    def search_flights(self, departure: str = None, arrival: str = None, page: int = 1, page_size: int = 5) -> None:
        """Search for flights based on departure and/or arrival locations with pagination."""
        offset = (page - 1) * page_size
        if departure and arrival:
            query = "SELECT * FROM flight WHERE departure = %s AND arrival = %s ORDER BY departuretime LIMIT %s OFFSET %s"
            params = (departure, arrival, page_size, offset)
        elif departure:
            query = "SELECT * FROM flight WHERE departure = %s ORDER BY departuretime LIMIT %s OFFSET %s"
            params = (departure, page_size, offset)
        elif arrival:
            query = "SELECT * FROM flight WHERE arrival = %s ORDER BY departuretime LIMIT %s OFFSET %s"
            params = (arrival, page_size, offset)
        else:
            print("Please specify at least one search criteria")
            return

        result = self.db.execute_query(query, params)
        self._display_search_results(result, page)
        if result:
            self.last_searched_route = {'departure': departure, 'arrival': arrival}

    def search_flights_advanced(self, date: str = None, departure: str = None, arrival: str = None, page: int = 1, page_size: int = 5) -> None:
        """Search for flights by date, departure, and/or arrival locations with pagination."""
        offset = (page - 1) * page_size
        query = "SELECT * FROM flight WHERE 1=1"
        params = []
        if date:
            query += " AND DATE(departuretime) = %s"
            params.append(date)
        if departure:
            query += " AND departure = %s"
            params.append(departure)
        if arrival:
            query += " AND arrival = %s"
            params.append(arrival)
        query += " ORDER BY departuretime LIMIT %s OFFSET %s"
        params.extend([page_size, offset])
        result = self.db.execute_query(query, tuple(params))
        self._display_search_results(result, page)
        if result:
            self.last_searched_route = {'departure': departure, 'arrival': arrival}

    def _display_search_results(self, result, page):
        """Display search results in a formatted table."""
        if result:
            print(f"\nSearch Results (Page {page}):")
            print("Flight\tFrom\tTo\tDeparture\tArrival\tStatus\tAvailable Seats\tDistance(km)\tDuration(min)\tStops\tFare($)")
            for row in result:
                print(f"{row[0]}{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[8]}\t{row[7]}\t{row[9]}\t{row[10]}\t{row[11]}\t{row[12]}")
        else:
            print("No flights found matching the criteria") 