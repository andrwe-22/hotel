# routes.py
import json
from datetime import datetime

from flask import render_template, request, redirect, url_for, session


from app import app, cursor, mysql, db ,Settings
from models import CustomData, Users, Rooms, Hostels, Bookings

from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify


def get_room_id_by_name(room_number):
    # Query the database to retrieve the room ID based on the room number
    query = "SELECT id FROM rooms WHERE room_number = %s"
    cursor.execute(query, (room_number,))
    room = cursor.fetchone()

    if room:
        return room['id']  # Return the room ID if found
    else:
        # Handle the case when the room number is not found
        # You can return None or an appropriate default value
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        # Query the database for the user
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        # Check if the user exists and the password is correct
        if user and check_password_hash(user['password'], password):
            # Store username, user_id, and logged_in status in the session
            session['logged_in'] = True
            session['username'] = user['name']  # Store the user's name in the session
            session['user_id'] = user['id']  # Store the user's ID in the session
            return redirect(url_for('index'))  # Redirect to the admin page after successful login

    return render_template('login.html')


# ваш код для роута /login

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        name = request.form['name']  # Extract the user's name

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Insert user information into the database, including the name
        query = "INSERT INTO users (username, password, name) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, hashed_password, name))
        mysql.commit()

        # Directly redirect to the index page after successful registration
        session['logged_in'] = True
        return redirect(url_for('login'))

    return render_template('registration.html')



@app.route('/update_settings', methods=['POST'])
def update_settings():
    enable_discounts = 'enable_discounts' in request.form
    enable_partial_discounts = 'enable_partial_discounts' in request.form

    Settings.query.filter_by(name='enable_discounts').update({'value': enable_discounts})
    Settings.query.filter_by(name='enable_partial_discounts').update({'value': enable_partial_discounts})
    db.session.commit()

    return redirect('/admin')

import random  # for simulating hostel occupancy
# Update the /book route to calculate the total price after discount
@app.route('/book', methods=['POST'])
def book():
    room_name = request.form['room']
    room_id = get_room_id_by_name(room_name)

    check_in = request.form['check-in']
    check_out = request.form['check-out']
    guests = int(request.form['guests'])

    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('login'))

    if room_id is None:
        return render_template('booking_error.html', message="Room not found")

    room = Rooms.query.get(room_id)
    if room is None:
        return render_template('booking_error.html', message="Room not found")

    price_per_night = float(room.price_per_night)
    duration_in_days = (datetime.strptime(check_out, '%Y-%m-%d') - datetime.strptime(check_in, '%Y-%m-%d')).days

    hostel_occupancy = random.uniform(0, 1)
    discount = 0.0

    enable_discounts = Settings.query.filter_by(name='enable_discounts').first().value
    enable_partial_discounts = Settings.query.filter_by(name='enable_partial_discounts').first().value

    if enable_discounts:
        if hostel_occupancy < 0.35:
            discount += 0.14
        elif hostel_occupancy < 0.5:
            discount += 0.07

        if enable_partial_discounts:
            if duration_in_days > 5 and duration_in_days <= 10:
                discount += 0.05
            elif duration_in_days > 10:
                discount += 0.07

            if guests > 3:
                discount += 0.05

            if datetime.now().month == 12:
                discount += 0.05

            if discount > 0.17:
                discount = 0.17

    total_price = price_per_night * duration_in_days * guests * (1 - discount)

    new_booking = Bookings(user_id=user_id, room_id=room_id, check_in_date=check_in, check_out_date=check_out, guests=guests, price=total_price, discount=discount)
    db.session.add(new_booking)
    db.session.commit()

    return render_template('booking_success.html')

def get_room_id_by_name(room_name):
    room = Rooms.query.filter_by(room_number=room_name).first()
    return room.id if room else None
@app.route('/book', methods=['POST'])
def book_room():
    if request.method == 'POST':
        room_name = request.form['room']
        room_id = get_room_id_by_name(room_name)

        check_in = request.form['check-in']
        check_out = request.form['check-out']
        guests = int(request.form['guests'])

        user_id = session.get('user_id')

        if user_id is None:
            return redirect(url_for('login'))

        query = "INSERT INTO bookings (user_id, room_id, check_in_date, check_out_date, guests) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (user_id, room_id, check_in, check_out, guests))
        mysql.commit()

        return render_template('booking_success.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Clear the session
    return redirect(url_for('login'))

# Index Route - Displayed after successful login
# Update the index route to fetch comments from the database and pass them to the template

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))  # Redirect unauthorized users to login




    # Fetch comments from the database
    cursor.execute("SELECT * FROM comments")
    comments = cursor.fetchall()


    # Render the index page with comments
    return render_template('index.html', comments=comments)



@app.route('/bookings')
def booking():
    return render_template('bookings.html')

@app.route('/booking_success')
def booking_success():
    return render_template('booking_success.html')

# Update the Flask route for adding comments
# Update the add_comment route to properly insert comments into the database
@app.route('/add_comment', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        new_comment = request.form['new-comment']
        user_id = session.get('user_id')

        # Insert the new comment into the database
        query = "INSERT INTO comments (user_id, comment) VALUES (%s, %s)"
        cursor.execute(query, (user_id, new_comment,))
        mysql.commit()

        return redirect(url_for('index'))  # Redirect to the index page after adding the comment

# Redirect to the index page after adding the comment


# Update the existing '/add_room' route to handle adding rooms to hotels
@app.route('/add_room', methods=['POST'])
def add_room():
    if request.method == 'POST':
        room_number = request.form['room_number']
        description = request.form['description']
        price_per_night = request.form['price_per_night']
        hotel_id = request.form['hotel_id']  # Get the hotel ID from the form

        query = "INSERT INTO rooms (room_number, description, price_per_night, hotel_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (room_number, description, price_per_night, hotel_id))
        mysql.commit()

        return redirect(url_for('index'))  # Redirect to the index page after adding the room


#room1
@app.route('/viproom')
def viproom():
    return render_template('viproom.html')
#room2
@app.route('/Standardroom')
def standard_room():
    return render_template('Standardroom.html')

#room3

@app.route('/Doubleroom')
def double_room():
    return render_template('Doubleroom.html')
#room4
@app.route('/Suiteroom')
def suite_room():
    return render_template('Suiteroom.html')




# Update the get_room_price() function to use SQLAlchemy queries

def serialize_room(room):
    """Convert a Room object to a dictionary."""
    return {
        'id': room.id,
        'room_number': room.room_number,
        'description': room.description,
        'price_per_night': room.price_per_night,
        'quantity': room.quantity,
        'hotel_id': room.hotel_id
    }
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    # Check if the user is logged in
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Update settings based on admin input
        enable_discounts = request.form.get('enable_discounts') == 'on'
        enable_partial_discounts = request.form.get('enable_partial_discounts') == 'on'

        discount_setting = Settings.query.filter_by(name='enable_discounts').first()
        discount_setting.value = enable_discounts

        partial_discount_setting = Settings.query.filter_by(name='enable_partial_discounts').first()
        partial_discount_setting.value = enable_partial_discounts

        db.session.commit()

    # Retrieve settings for display
    settings = Settings.query.all()

    # Get data for the admin dashboard
    users = Users.query.all()
    rooms = Rooms.query.all()
    hostels = Hostels.query.all()
    bookings = Bookings.query.all()

    # Calculate booking data for each room
    room_bookings = []
    total_booked = 0
    total_rooms = 0

    for room in rooms:
        bookings_count = Bookings.query.filter_by(room_id=room.id).count()
        total_booked += bookings_count
        total_rooms += room.quantity
        room_bookings.append((room, bookings_count))

    # Calculate overall occupancy rate
    overall_occupancy = round((total_booked / total_rooms) * 100, 2) if total_rooms > 0 else 0

    # Prepare data for the chart
    room_numbers = [room.room_number for room, _ in room_bookings] + ['All Rooms']
    booking_percentages = [round((bookings_count / room.quantity) * 100, 2) if room.quantity > 0 else 0 for room, bookings_count in room_bookings] + [overall_occupancy]

    # Convert room bookings to a JSON serializable format
    room_bookings_serializable = [(serialize_room(room), bookings_count) for room, bookings_count in room_bookings]
    room_bookings_json = json.dumps(room_bookings_serializable)

    # Pass data to the template
    return render_template('admin.html', users=users, rooms=rooms, hostels=hostels, bookings=bookings, settings=settings, room_bookings=room_bookings, room_numbers=room_numbers, booking_percentages=booking_percentages, room_bookings_json=room_bookings_json, overall_occupancy=overall_occupancy)


# Route for the admin page
@app.route('/admin')
def admin():
    users = Users.query.all()
    rooms = Rooms.query.all()
    hostels = Hostels.query.all()
    bookings = Bookings.query.all()
    settings = Settings.query.all()
    return render_template('admin.html', users=users, rooms=rooms, hostels=hostels, bookings=bookings, settings=settings)

@app.route('/admin', methods=['GET'])
def admin_page():
    # Получаем список комнат и данные о бронировании из базы данных
    rooms = Rooms.query.all()

    # Вычисляем данные о бронировании для каждой комнаты
    room_bookings = []
    for room in rooms:
        # Получаем количество бронирований для данной комнаты
        bookings_count = Bookings.query.filter_by(room_id=room.id).count()
        # Добавляем данные о комнате и количестве бронирований в список
        room_bookings.append((room, bookings_count))

    # передаем данные на шаблон admin.html
    return render_template('admin.html', room_bookings=room_bookings)


# Route to handle form submission for modifying data
@app.route('/update_data', methods=['POST'])
def update_data():
    data_id = request.form.get('data_id')  # Assuming there's a form field named data_id
    new_data_value = request.form.get('new_data_value')  # Assuming there's a form field for the new data value

    # Assuming you have a Data model and you're using SQLAlchemy
    data_to_update = db.query.get(data_id)
    if data_to_update:
        data_to_update.data_field = new_data_value  # Update the data field with the new value
        db.session.commit()
        # Data successfully updated, redirect to admin page or success page
        return redirect('/admin')
    else:
        # Data with provided ID not found, redirect to an error page or handle it accordingly
        return redirect('/error')

# app.py
@app.route('/add_data', methods=['POST'])
def add_data():
    data_type = request.form.get('data_type')  # Assuming there's a form field for selecting data type
    if data_type == 'user':
        # Extract user data from the form
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']

        # Insert user data into the Users table
        new_user = Users(username=username, password=password, name=name)
        db.session.add(new_user)
        db.session.commit()
    elif data_type == 'room':
        # Extract room data from the form
        room_number = request.form['room_number']
        description = request.form['description']
        price_per_night = request.form['price_per_night']
        quantity = request.form['quantity']  # Ensure quantity is retrieved
        hotel_id = request.form['hotel_id']

        # Insert room data into the Rooms table
        new_room = Rooms(room_number=room_number, description=description, price_per_night=price_per_night, quantity=quantity, hotel_id=hotel_id)
        db.session.add(new_room)
        db.session.commit()
    elif data_type == 'hostel':
        # Extract hostel data from the form
        name = request.form['name']
        address = request.form['address']
        phone_number = request.form['phone_number']
        email = request.form['email']

        # Insert hostel data into the Hostels table
        new_hostel = Hostels(name=name, address=address, phone_number=phone_number, email=email)
        db.session.add(new_hostel)
        db.session.commit()
    elif data_type == 'booking':
        # Extract booking data from the form
        user_id = request.form['user_id']
        room_id = request.form['room_id']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        guests = request.form['guests']
        discount = request.form.get('discount')  # Optional field

        # Insert booking data into the Bookings table
        new_booking = Bookings(user_id=user_id, room_id=room_id, check_in_date=check_in_date, check_out_date=check_out_date, guests=guests, discount=discount)
        db.session.add(new_booking)
        db.session.commit()

    return redirect('/admin')  # Redirect to the admin page after adding the data

@app.route('/delete_data', methods=['POST'])
def delete_data():
    data_id = request.form.get('data_id')
    data_type = request.form.get('data_type')

    if data_type == 'user':
        user_to_delete = Users.query.get(data_id)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
    elif data_type == 'room':
        room_to_delete = Rooms.query.get(data_id)
        if room_to_delete:
            db.session.delete(room_to_delete)
            db.session.commit()
    elif data_type == 'hostel':
        hostel_to_delete = Hostels.query.get(data_id)
        if hostel_to_delete:
            db.session.delete(hostel_to_delete)
            db.session.commit()

    elif data_type == 'booking':
        booking_to_delete = Bookings.query.get(data_id)
        if booking_to_delete:
            db.session.delete(booking_to_delete)
            db.session.commit()

    return redirect('/admin')

@app.route('/update_price', methods=['POST'])
def update_price():
    room_id = request.form['room_id']
    new_price = request.form['new_price']

    room_to_update = Rooms.query.get(room_id)
    if room_to_update:
        room_to_update.price_per_night = new_price
        db.session.commit()

    return redirect('/admin')



@app.route('/api/room/<int:room_id>', methods=['GET'])
def get_room(room_id):
    room = Rooms.query.get(room_id)
    if room:
        room_data = {
            'room_number': room.room_number,
            'description': room.description,
            'price_per_night': str(room.price_per_night),
            'quantity': room.quantity,
            'hotel_id': room.hotel_id
        }
        return jsonify(room_data)
    else:
        return jsonify({'error': 'Room not found'}), 404


