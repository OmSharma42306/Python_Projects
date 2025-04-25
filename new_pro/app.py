from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize DB
def init_db():
    if not os.path.exists('tickets.db'):
        conn = sqlite3.connect('tickets.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ticket (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                match_date TEXT NOT NULL,
                match_time TEXT NOT NULL,
                match_teams TEXT NOT NULL,
                match_venue TEXT NOT NULL,
                seat_price INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = generate_password_hash(request.form['password'])
        conn = sqlite3.connect('tickets.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)', (name, email, phone, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return render_template('signup.html', msg='Email already exists')
        conn.close()
        return redirect('/signin')
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('tickets.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[4], password):
            session['user_id'] = user[0]
            return redirect('/tickets')
        else:
            return render_template('signin.html', msg='Invalid credentials')
    return render_template('signin.html')

@app.route('/tickets')
def tickets():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Ticket')
    tickets = cursor.fetchall()
    conn.close()
    return render_template('tickets.html', tickets=tickets)

@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    if 'user_id' not in session:
        return redirect('/signin')

    data = request.get_json()
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Ticket (name, match_date, match_time, match_teams, match_venue, seat_price)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['name'], data['match_date'], data['match_time'], data['match_teams'], data['match_venue'], data['seat_price']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Ticket booked successfully!'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
