from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import sqlite3
import time
import razorpay
import smtplib
from reportlab.pdfgen import canvas
import uuid
import os
from email.message import EmailMessage
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
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
ADMIN_USERNAME = "admin@gmail.com"
ADMIN_PASSWORD = "admin123"

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
            print("Login Route",email)
            session['user_email'] = email
            return render_template('tickets.html')
        else:
            
            return render_template('user_login.html', msg='Invalid credentials!')
    # return render_template('index.html')
    return render_template('user_login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/back')
def back():
    return render_template('tickets.html')

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
    
@app.route('/getticket')
def getticket():
    user_email = session.get('user_email')  # Make sure to store email earlier in session
    pdf_path = session.get('pdf_path')
    if not user_email:
        return "Email not found. Booking incomplete.", 400

    msg = EmailMessage()
    msg['Subject'] = 'Your Match Ticket'
    msg['From'] = 'codingwithak6@gmail.com'
    msg['To'] = user_email
    msg.set_content('Thanks for booking with us! Your ticket is attached.')

    try:
        with open(pdf_path, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype='application', subtype='pdf', filename='Match_Ticket.pdf')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('codingwithak6@gmail.com', 'didr yqlz bhwe gjwi')
            smtp.send_message(msg)

        # Optionally clean up the file
        os.remove(pdf_path)

        return render_template('xyz.html', msg='Ticket sent to your email!')
    except Exception as e:
        print("Error sending email:", e)
        return render_template('xyz.html', msg='Failed to send email.')

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

    # PDF generation inside book_ticket
    ticket_width = 160 * mm
    ticket_height = 60 * mm
     # Create PDF ticket
    pdf_filename = f"{uuid.uuid4()}.pdf"
    pdf_path = os.path.join("temp_tickets", pdf_filename)
    
    c = canvas.Canvas(pdf_path, pagesize=(ticket_width, ticket_height))

# Background rectangle (ticket border)
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(2)
    c.rect(5 * mm, 5 * mm, ticket_width - 10 * mm, ticket_height - 10 * mm, stroke=1, fill=0)

# Header
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(ticket_width / 2, ticket_height - 15 * mm, "MATCH TICKET")

# Event Info
    c.setFont("Helvetica", 11)
    c.drawString(15 * mm, ticket_height - 30 * mm, f"Name: {name}")
    c.drawString(15 * mm, ticket_height - 38 * mm, f"Teams: {match_teams}")
    c.drawString(15 * mm, ticket_height - 46 * mm, f"Date: {match_date}")
    c.drawString(15 * mm, ticket_height - 54 * mm, f"Time: {match_time}")
    print("price",seat_price)
# Venue & Price
    c.drawString(90 * mm, ticket_height - 30 * mm, f"Venue: {match_venue}")
    c.drawString(90 * mm, ticket_height - 45 * mm, f"Price: ₹{seat_price}")

# Footer line or barcode placeholder
    # c.setStrokeColor(colors.lightgrey)
    # c.line(15 * mm, 15 * mm, ticket_width - 15 * mm, 15 * mm)

    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(ticket_width / 2, 8 * mm, "Thank you for booking with us!")

    c.save()

    session['pdf_path'] = pdf_path

    return jsonify({'message': 'Ticket booked successfully!'})


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
