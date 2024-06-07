# dp_init.py

import os
import mysql.connector
from flask import json
from app import app
from models import db, Settings

def initialize_database():
    # Connect to the database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='hotel'
    )

    # MySQL configurations
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'hotel'

    # Initialize MySQL
    try:
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
        )
        print("Connected to the database successfully.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

    cursor = connection.cursor(dictionary=True)

    # Initialize an empty list to store comments
    comments = []

    # Load comments from a file if it exists, otherwise initialize an empty list
    file_path = 'comments.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            comments = json.load(file)

    # Create Users table in the database
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL
        )
    """)
    connection.commit()

    # Create Rooms table in the database
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room_number INT NOT NULL,
            description TEXT,
            price_per_night DECIMAL(10, 2) NOT NULL,
            quantity INT NOT NULL DEFAULT 1,
            hotel_id INT,
            FOREIGN KEY (hotel_id) REFERENCES hostels(id)
        )
    """)
    connection.commit()

    # Create Hostels table in the database
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hostels (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            phone_number VARCHAR(20) NOT NULL,
            email VARCHAR(255) NOT NULL
        )
    """)
    connection.commit()

    # Create Bookings table in the database
    cursor.execute("""
         CREATE TABLE IF NOT EXISTS bookings (
             id INT AUTO_INCREMENT PRIMARY KEY,
             user_id INT NOT NULL,
             room_id INT NOT NULL,
             check_in_date DATE NOT NULL,
             check_out_date DATE NOT NULL,
             guests INT NOT NULL,
             discount DECIMAL(10, 2),
             price DECIMAL(10, 2) NOT NULL,
             discounted_price DECIMAL(10, 2),
             settings_id INT,  # Добавлено новое поле для внешнего ключа
             FOREIGN KEY (user_id) REFERENCES users(id),
             FOREIGN KEY (room_id) REFERENCES rooms(id),
            
         )
    """)
    connection.commit()

    # Create Settings table in the database
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            value BOOLEAN NOT NULL
        )
    """)
    connection.commit()

    # Insert default settings if they do not exist
    cursor.execute("SELECT COUNT(*) as count FROM settings")
    count = cursor.fetchone()['count']
    if count == 0:
        cursor.execute("INSERT INTO settings (name, value) VALUES ('enable_discounts', TRUE)")
        cursor.execute("INSERT INTO settings (name, value) VALUES ('enable_partial_discounts', TRUE)")
        connection.commit()

    cursor.close()
    connection.close()

def initialize_database():
    with app.app_context():
        db.create_all()

        # Check if settings already exist to avoid duplicate entries
        if not Settings.query.first():
            default_settings = [
                Settings(name='enable_discounts', value=True),
                Settings(name='enable_partial_discounts', value=True)
            ]

            # Add settings individually
            for setting in default_settings:
                db.session.add(setting)
            try:
                db.session.commit()
                print("Database initialized with settings.")
            except Exception as e:
                db.session.rollback()
                print(f"Error initializing database settings: {e}")

if __name__ == '__main__':
    initialize_database()
