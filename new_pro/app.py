from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import sqlite3
import time
import razorpay
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management


client = razorpay.Client(auth=("rzp_test_xt0FlQyPwPEQZS", "bViBMXjdJjIYG9Fz9zGYF6nX"))
razorpay_key = "bViBMXjdJjIYG9Fz9zGYF6nX"





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


    # Bookings Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        ticket_id INTEGER NOT NULL,
        booking_time TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(ticket_id) REFERENCES Ticket(id)
    )
''')

    conn.commit()
    conn.close()



# Fake admin credentials for demo
ADMIN_USERNAME = "xyz123@gmail.com"
ADMIN_PASSWORD = "xyz"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid Credentials')
    
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/user_login',methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        conn = sqlite3.connect('tickets.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        conn.close()
        if email == "admin123@gmail.com" and password == "123456":
            return render_template('admin_dashboard.html')
        elif user:
            return render_template('tickets.html')
        else:
            return render_template('index.html', msg='Invalid credentials!')
    # return render_template('index.html')
    return render_template('user_login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        print(name,email)
        conn = sqlite3.connect('tickets.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, email, phone, password)
            VALUES (?, ?, ?, ?)
        ''', (name, email, phone, password))
        conn.commit()
        conn.close()
        return render_template('user_login.html',msg='Signup successful!')
    return render_template('signup.html')
    #return render_template('signup.html')

@app.route('/getticket')
def getticket():
    time.sleep(5)
    # import telepot
    # bot = telepot.Bot("7973668926:AAE4xaadr4YaB3LjL_pBw8vhHl2IFnE6FR4")
    # chat_id = "5514657308"
    # bot.sendDocument(chat_id, open('C:/Users/Akash B N/Downloads/ticket.pdf', 'rb'))
    return render_template('xyz.html',msg='Ticket sent to your telegram!')

@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.get_json()
    amount = int(data['amount']) * 100  # Convert to paise

    order = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': '1'
    })

    return jsonify(order)


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
# @app.route('/create_order', methods=['POST'])
# def create_razorpay_order():
#     data = request.get_json()
#     #amount = int(data['seat_price']) * 100  # in paise
#     amount = int(data['amount']) * 100  # Convert to paise
#     name = data['name']
#     match_date = data['match_date']
#     match_time = data['match_time']
#     match_teams = data['match_teams']
#     match_venue = data['match_venue']
#     quantity = data.get('quantity', 1)

#     # Save ticket temporarily if needed or just pass data for now

#     order = client.order.create({
#         'amount': amount,
#         'currency': 'INR',
#         'payment_capture': '1'
#     })

#     return {
#         'order_id': order['id'],
#         'amount': amount,
#         'razorpay_key': razorpay_key,
#         'ticket_info': {
#             'name': name,
#             'match_date': match_date,
#             'match_time': match_time,
#             'match_teams': match_teams,
#             'match_venue': match_venue,
#             'quantity': quantity
#         }
#     }




@app.route('/buy_ticket/<int:ticket_id>', methods=['GET'])
def buy_ticket(ticket_id):
    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT seat_price, match_teams FROM Ticket WHERE id = ?", (ticket_id,))
    ticket = cursor.fetchone()
    conn.close()

    if not ticket:
        return "Ticket not found", 404

    amount = ticket[0] * 100  # Razorpay uses paise
    match_teams = ticket[1]

    # Razorpay order creation
    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    return render_template("checkout.html", 
                           amount=amount, 
                           razorpay_key=razorpay_key, 
                           order_id=order['id'],
                           ticket_id=ticket_id,
                           match_teams=match_teams)



@app.route('/payment_success', methods=['POST'])
def payment_success():
    data = request.get_json()
    user_id = session.get('user_id')
    ticket_id = data['ticket_id']

    # You can verify signature here using:
    # razorpay_client.utility.verify_payment_signature(...)

    # Save the booking
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Bookings (user_id, ticket_id)
        VALUES (?, ?)
    ''', (user_id, ticket_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Payment successful and ticket booked!'})


@app.route('/viewBookings')
def viewBookings():
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    # Fetch all ticket details
    cursor.execute('SELECT * FROM Ticket')
    tickets = cursor.fetchall()
    print("TO",tickets)
    conn.close()

    # Create a list of dictionaries for easier rendering in HTML
    tickets_list = [
        {
            'ticket_id': ticket[0],
            'ticket_name': ticket[1],
            'match_date': ticket[2],
            'match_time': ticket[3],
            'match_teams': ticket[4],
            'match_venue': ticket[5],
            'seat_price': ticket[6]
        }
        for ticket in tickets
    ]

    return render_template('admin_view_bookings.html', tickets=tickets_list)




if __name__ == '__main__':
    app.run(debug=True)
