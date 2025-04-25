from flask import Flask, render_template, request, jsonify
import sqlite3
import telepot
import time
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def init_db():
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
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    data = request.get_json()  # Get JSON data from the request
    name = data['name']
    match_date = data['match_date']
    match_time = data['match_time']
    match_teams = data['match_teams']
    match_venue = data['match_venue']
    seat_price = data['seat_price']

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Ticket (name, match_date, match_time, match_teams, match_venue, seat_price)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, match_date, match_time, match_teams, match_venue, seat_price))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Ticket booked successfully!'})

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        conn = sqlite3.connect('tickets.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, email, phone, password)
            VALUES (?, ?, ?, ?)
        ''', (name, email, phone, password))
        conn.commit()
        conn.close()
        return render_template('index.html',msg='Signup successful!')
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('tickets.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return render_template('tickets.html')
        else:
            return render_template('index.html', msg='Invalid credentials!')
    return render_template('index.html')

@app.route('/tickets')
def tickets():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Ticket')
    tickets = cursor.fetchall()
    conn.close()

    tickets_list = [{'name': ticket[1], 'match_date': ticket[2], 'match_time': ticket[3], 'match_teams': ticket[4], 'match_venue': ticket[5], 'seat_price': ticket[6]} for ticket in tickets]
    return jsonify(tickets_list)

@app.route('/getticket')
def getticket():
    time.sleep(5)
    import telepot
    bot = telepot.Bot("7973668926:AAE4xaadr4YaB3LjL_pBw8vhHl2IFnE6FR4")
    chat_id = "5514657308"
    bot.sendDocument(chat_id, open('C:/Users/Akash B N/Downloads/ticket.pdf', 'rb'))
    return render_template('index.html',msg='Ticket sent to your telegram!')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

    