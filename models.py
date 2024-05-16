# models.py

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__, template_folder='templates')
app.secret_key = 'root'  # Необходимо изменить на ваш секретный ключ

# Настройки базы данных SQLAlchemy


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    bookings = db.relationship('Bookings', backref='user', lazy=True)

class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    price_per_night = db.Column(db.DECIMAL(10, 2), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hostels.id'))  # Add this line
    bookings = db.relationship('Bookings', backref='room', lazy=True)

class Hostels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)

class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.DECIMAL(10, 2))



if __name__ == '__main__':
    app.run(debug=True)
class CustomData:
    query = None