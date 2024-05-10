# routes.py
from datetime import datetime

from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, cursor, mysql

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
            return redirect(url_for('index'))

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
            # Handle the case when the room is not found, for example, redirect to an error page
            return render_template('booking_success.html')

        query = "INSERT INTO bookings (user_id, room_id, check_in_date, check_out_date, guests) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (user_id, room_id, check_in, check_out, guests))
        mysql.commit()

        duration_in_days = (datetime.strptime(check_out, '%Y-%m-%d') - datetime.strptime(check_in, '%Y-%m-%d')).days

        discount = 0.0  # Default discount is 0%

        # Apply discount based on the duration of stay
        if duration_in_days > 5 and duration_in_days <= 10:
            discount = 0.05  # 5% discount for stays longer than 5 days but less than or equal to 10 days
        elif duration_in_days > 10:
            discount = 0.10  # 10% discount for stays longer than 10 days

        # Update the discount in the database for the current booking
        query_discount = "UPDATE bookings SET discount = %s WHERE id = %s"
        cursor.execute(query_discount, (discount, cursor.lastrowid))
        mysql.commit()

        return render_template('booking_success.html')

    # Handle other HTTP methods or redirect to the booking form if not a POST request
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