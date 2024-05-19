# routes.py

from datetime import datetime

from flask import render_template, request, redirect, url_for, session


from app import app, cursor, mysql, db
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
import random  # for simulating hostel occupancy

# Update the /book route to calculate the total price after discount
@app.route('/book', methods=['POST'])
def book():
    if request.method == 'POST':
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

        # Retrieve the room price
        cursor.execute("SELECT price_per_night FROM rooms WHERE id = %s", (room_id,))
        room = cursor.fetchone()
        if room is None:
            return render_template('booking_error.html', message="Room not found")

        # Convert price_per_night to float before calculation
        price_per_night_float = float(room['price_per_night'])

        # Calculate total duration of stay in days
        duration_in_days = (datetime.strptime(check_out, '%Y-%m-%d') - datetime.strptime(check_in, '%Y-%m-%d')).days

        # Simulate hostel occupancy (for demonstration purposes)
        hostel_occupancy = random.uniform(0, 1)  # Simulating occupancy percentage (between 0 and 1)

        # Calculate discount based on hostel occupancy
        if hostel_occupancy >= 0.6:  # 60% or more occupancy
            discount = 0.25
        elif hostel_occupancy >= 0.35:  # 35% or more occupancy
            discount = 0.15
        else:
            discount = 0.0

        # Apply additional discounts based on other conditions

        # Discount based on duration
        if duration_in_days > 5 and duration_in_days <= 10:
            discount += 0.05
        elif duration_in_days > 10:
            discount += 0.10

        # Discount for high number of guests
        if guests > 5:
            discount += 0.05

        # Check if it's a holiday period (for demonstration purposes, let's assume Christmas)
        if datetime.now().month == 12:  # December (Christmas)
            discount += 0.05

        # Calculate the total price after discount
        total_price = price_per_night_float * duration_in_days * guests * (1 - discount)

        # Insert booking into the database including the price and discount
        query = "INSERT INTO bookings (user_id, room_id, check_in_date, check_out_date, guests, price, discount) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (user_id, room_id, check_in, check_out, guests, total_price, discount))
        mysql.commit()

        return render_template('booking_success.html')

    return redirect(url_for('booking_form'))


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


@app.route('/admin')
def admin_dashboard():
    # Check if the user is logged in
    if 'logged_in' not in session:
        return redirect(url_for('login'))  # Redirect unauthorized users to login

    # Получаем данные для отображения в админской панели
    users = Users.query.all()
    rooms = Rooms.query.all()
    hostels = Hostels.query.all()
    bookings = Bookings.query.all()

    # Передаем данные на шаблон admin.html
    return render_template('admin.html', users=users, rooms=rooms, hostels=hostels, bookings=bookings)




# Route for the admin page
@app.route('/admin')
def admin():
    # Получаем данные для отображения в админской панели
    users = Users.query.all()
    rooms = Rooms.query.all()
    hostels = Hostels.query.all()
    bookings = Bookings.query.all()

    # Передаем данные на шаблон admin.html
    return render_template('admin.html', users=users, rooms=rooms, hostels=hostels, bookings=bookings)

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
        quantity = request.form['quantity']
        hotel_id = request.form['hotel_id']

        # Insert room data into the Rooms table
        new_room = Rooms(room_number=room_number, description=description, price_per_night=price_per_night,  quantity=quantity , hotel_id=hotel_id)
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
        new_booking = Bookings(user_id=user_id, room_id=room_id, check_in_date=check_in_date,
                               check_out_date=check_out_date, guests=guests, discount=discount)
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


