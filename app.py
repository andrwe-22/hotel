# app.py

import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import secrets
import json
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = secrets.token_hex(16)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'hotel'

# Set the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/hotel'

# Initialize MySQL
try:
    # Attempt to connect to the database
    mysql = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
    )
    print("Connected to the database successfully.")
except Exception as e:
    print(f"Error connecting to the database: {e}")


# Create a cursor to interact with the database
cursor = mysql.cursor(dictionary=True)

# Initialize an empty list to store comments
comments = []

# Load comments from a file if it exists, otherwise initialize an empty list
file_path = 'comments.json'
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        comments = json.load(file)

# Initialize SQLAlchemy
db = SQLAlchemy(app)
