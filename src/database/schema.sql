-- Create database if not exists
CREATE DATABASE IF NOT EXISTS flightproject;
USE flightproject;

-- Admin table
CREATE TABLE IF NOT EXISTS admin (
    name VARCHAR(50) PRIMARY KEY,
    password INT NOT NULL
);

-- Job table
CREATE TABLE IF NOT EXISTS job (
    job_id INT PRIMARY KEY,
    job_title VARCHAR(50) NOT NULL,
    salary DECIMAL(10,2) NOT NULL
);

-- Employee table
CREATE TABLE IF NOT EXISTS employee (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    sales INT NOT NULL,
    job_id INT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES job(job_id)
);

-- Employee password table
CREATE TABLE IF NOT EXISTS employeepass (
    name VARCHAR(50) PRIMARY KEY,
    password INT NOT NULL
);

-- Flight table
CREATE TABLE IF NOT EXISTS flight (
    flightseries VARCHAR(10) NOT NULL,
    flightnumber INT NOT NULL,
    departure VARCHAR(50) NOT NULL,
    arrival VARCHAR(50) NOT NULL,
    departuretime DATETIME NOT NULL,
    arrivaltime DATETIME NOT NULL,
    totalseats INT NOT NULL,
    available INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    PRIMARY KEY (flightseries, flightnumber)
);

-- Passenger accounts table
CREATE TABLE IF NOT EXISTS passenger_accounts (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(64) NOT NULL,  -- For storing hashed passwords
    email VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL
);

-- Seats table
CREATE TABLE IF NOT EXISTS seats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_series VARCHAR(10) NOT NULL,
    flight_number INT NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (flight_series, flight_number) 
        REFERENCES flight(flightseries, flightnumber)
        ON DELETE CASCADE,
    UNIQUE KEY unique_seat (flight_series, flight_number, seat_number)
);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    booking_id VARCHAR(8) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    flight_series VARCHAR(10) NOT NULL,
    flight_number INT NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    booking_date DATETIME NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'CONFIRMED',
    FOREIGN KEY (username) 
        REFERENCES passenger_accounts(username)
        ON DELETE CASCADE,
    FOREIGN KEY (flight_series, flight_number) 
        REFERENCES flight(flightseries, flightnumber)
        ON DELETE CASCADE,
    FOREIGN KEY (flight_series, flight_number, seat_number) 
        REFERENCES seats(flight_series, flight_number, seat_number)
        ON DELETE CASCADE
);

-- Passenger table (for historical records)
CREATE TABLE IF NOT EXISTS passenger (
    flightserial VARCHAR(10) NOT NULL,
    flightnumber INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    passportserial VARCHAR(10) NOT NULL,
    passportnumber INT NOT NULL,
    dob DATE NOT NULL,
    passportdoi DATE NOT NULL,
    passportdoe DATE NOT NULL,
    visano INT NOT NULL,
    PRIMARY KEY (passportserial, passportnumber),
    FOREIGN KEY (flightserial, flightnumber) 
        REFERENCES flight(flightseries, flightnumber)
        ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_booking_username ON bookings(username);
CREATE INDEX idx_booking_flight ON bookings(flight_series, flight_number);
CREATE INDEX idx_booking_status ON bookings(status);
CREATE INDEX idx_seat_availability ON seats(flight_series, flight_number, is_available);
CREATE INDEX idx_flight_dates ON flight(departuretime, arrivaltime);
CREATE INDEX idx_passenger_flight ON passenger(flightserial, flightnumber);

-- Insert default admin account
INSERT INTO admin (name, password) VALUES ('admin', 1234);

-- Insert some example jobs for test
INSERT INTO job (job_id, job_title, salary) VALUES 
(1, 'Manager', 5000.00),
(2, 'Sales Representative', 3000.00),
(3, 'Customer Service', 2500.00);

-- Insert example employee for test
INSERT INTO employee (emp_id, name, sales, job_id) VALUES 
(1, 'John Doe', 100, 1);

-- Insert example employee password for test
INSERT INTO employeepass (name, password) VALUES 
('John Doe', 1234);

-- Insert example flight for test for test
INSERT INTO flight (flightseries, flightnumber, departure, arrival, departuretime, arrivaltime, totalseats, available, status, price) VALUES 
('AA', 101, 'New York', 'London', '2024-03-20 10:00:00', '2024-03-20 22:00:00', 150, 150, 'ON TIME', 500.00);

-- Insert example seats for the flight for test
INSERT INTO seats (flight_series, flight_number, seat_number, is_available) VALUES 
('AA', 101, '1A', TRUE),
('AA', 101, '1B', TRUE),
('AA', 101, '1C', TRUE),
('AA', 101, '2A', TRUE),
('AA', 101, '2B', TRUE),
('AA', 101, '2C', TRUE); 