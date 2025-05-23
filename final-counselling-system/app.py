from flask import Flask, render_template, request, redirect, url_for, session,jsonify,flash
import sqlite3
import time
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)
app.secret_key = 'your_secret_key'  


def init_db():
    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS counsellors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        specialization TEXT NOT NULL,
        bio TEXT NOT NULL
    )
''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        counsellor_id INTEGER,
        message TEXT NOT NULL,
        reply TEXT,
        timestamp TEXT
    )
''')
    
    cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    counsellor_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL
)
''')


# # Insert fixed counsellors (only run once)
    # cursor.execute("SELECT COUNT(*) FROM counsellors")
    # if cursor.fetchone()[0] == 0:
    #         counsellor_data = [
    #     ("Praveen Ambala", "praveenkumar.ambala231@counsel.com", "praveen@123", "Academic","Helping students navigate Academic challenges with empathy and expertise."),
    #     ("Akash Tripathi", "akashatripathi.312@counsel.com", "akash@123", "Career","Helping students navigate Career challenges with empathy and expertise."),
    #     ("Satyam Shubham", "satyamshubham.442@counsel.com", "satyam@123", "Personal","Helping students navigate Personal challenges with empathy and expertise."),
    #     ("Dilip Kapoor", "dilipkapoor.331@counsel.com", "dilip@123", "Health","Helping students navigate Health challenges with empathy and expertise."),
    #     ("Sagar Shnidhe", "sagarshindhe.351@counsel.com", "sagar@123", "Financial","Helping students navigate Financial challenges with empathy and expertise.")
    # ]
    # cursor.executemany("INSERT INTO counsellors (name, email, password, specialization,bio) VALUES (?, ?, ?, ?,?)", counsellor_data)

    #cursor.execute('ALTER TABLE counsellors ADD COLUMN bio TEXT')  # Run only once
    
    #cursor.execute('ALTER TABLE bookings ADD COLUMN scheduled_time TEXT')  # Run only once

    cursor.execute("PRAGMA table_info(counsellors)")
    columns = [column[1] for column in cursor.fetchall()]

    # if 'gender' not in columns:
    #     cursor.execute("ALTER TABLE counsellors ADD COLUMN gender TEXT")

    # if 'experience' not in columns:
    #     cursor.execute("ALTER TABLE counsellors ADD COLUMN experience TEXT")

    # if 'gender' not in columns:
    #     cursor.execute("ALTER TABLE users ADD COLUMN gender TEXT")
    # if 'counselling_type' not in columns:
    #     cursor.execute("ALTER TABLE users ADD COLUMN counselling_type TEXT")
    # if 'bio' not in columns:
    #     cursor.execute("ALTER TABLE users ADD COLUMN bio TEXT")
    # if 'caste' not in columns:
    #     cursor.execute("ALTER TABLE users ADD COLUMN caste TEXT")
    # if 'aadhaar' not in columns:
    #     cursor.execute("ALTER TABLE users ADD COLUMN aadhaar TEXT")
    # cursor.execute("ALTER TABLE users ADD COLUMN gender TEXT")
    #cursor.execute("ALTER TABLE users ADD COLUMN bio TEXT")

    
    conn.commit()
    conn.close()



# Fake admin credentials for demo
ADMIN_USERNAME = "xyz123@gmail.com"
ADMIN_PASSWORD = "xyz"

@app.route('/')
def home():
    return render_template('home.html')



def send_email(to_email, subject, body):
    from_email = ""  
    from_password = ""

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, [to_email], msg.as_string())
        server.quit()
    except Exception as e:
        print("Email failed:", e)


@app.route('/student_profile', methods=['GET', 'POST'])
def student_profile():
    if 'user_email' not in session:
        return redirect(url_for('user_login'))

    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        gender = request.form['gender']
        counselling_type = request.form['counselling_type']
        bio = request.form['bio']
        caste = request.form['caste']
        aadhaar = request.form['aadhaar']

        cursor.execute('''
            UPDATE users
            SET gender = ?, counselling_type = ?, bio = ?, caste = ?, aadhaar = ?
            WHERE email = ?
        ''', (gender, counselling_type, bio, caste, aadhaar, session['user_email']))
        conn.commit()

    cursor.execute('SELECT name, email, phone, gender, counselling_type, bio, caste, aadhaar FROM users WHERE email = ?', (session['user_email'],))
    user = cursor.fetchone()
    conn.close()

    return render_template('student_profile.html', user=user)


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

    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, email, phone FROM users')
    students = cursor.fetchall()
    cursor.execute('SELECT name, email, specialization FROM counsellors')
    counsellors = cursor.fetchall()
    conn.close()

    return render_template('admin_dashboard.html', students=students, counsellors=counsellors)

@app.route('/view_bookings')
def view_bookings():
    return "Booking view under construction."



@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_email' not in session:
        return redirect(url_for('user_login'))

    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        gender = request.form['gender']
        counselling_type = request.form['counselling_type']
        bio = request.form['bio']
        caste = request.form['caste']
        aadhaar = request.form['aadhaar']

        cursor.execute('''
            UPDATE users SET gender = ?, counselling_type = ?, bio = ?, caste = ?, aadhaar = ?
            WHERE email = ?
        ''', (gender, counselling_type, bio, caste, aadhaar, session['user_email']))
        conn.commit()
        conn.close()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('student_dashboard'))

    # Fetch current data
    cursor.execute('SELECT gender, counselling_type, bio, caste, aadhaar FROM users WHERE email = ?', (session['user_email'],))
    data = cursor.fetchone()
    conn.close()
    return render_template('update_profile.html', data=data)


@app.route('/book_call/<int:counsellor_id>')
def book_call(counsellor_id):
    if 'user_email' not in session:
        return redirect(url_for('user_login'))

    
    student_email = session['user_email']
    
    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE email = ?', (student_email,))
    student_id = cursor.fetchone()[0]
    print(student_id)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO bookings (student_id, counsellor_id, timestamp)
        VALUES (?, ?, ?)
    ''', (student_id, counsellor_id, timestamp))
    conn.commit()
    conn.close()

    return redirect(url_for('select_counsellor'))



@app.route('/student_messages')
def student_messages():
    if 'user_email' not in session:
        return redirect(url_for('user_login'))

    student_email = session['user_email']

    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE email = ?', (student_email,))
    student = cursor.fetchone()

    if student:
        student_id = student[0]
        cursor.execute('''
            SELECT messages.message, messages.reply, counsellors.name
            FROM messages
            JOIN counsellors ON messages.counsellor_id = counsellors.id
            WHERE student_id = ?
        ''', (student_id,))
        messages = cursor.fetchall()
    else:
        messages = []

    conn.close()
    return render_template('student_messages.html', messages=messages)


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
        conn = sqlite3.connect('counsellors.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        conn.close()
        if email == "admin123@gmail.com" and password == "123456":
            return render_template('admin_dashboard.html')
        elif user:
            session['user_email'] = email
            #return render_template('student_dashboard.html')
            return redirect(url_for('student_dashboard'))
        else:
            return render_template('user_login.html', msg='Invalid credentials!')
    # return render_template('index.html')
    return render_template('user_login.html')



@app.route('/student_dashboard')
def student_dashboard():
    if 'user_email' not in session:
        return redirect(url_for('user_login'))
        #return render_template('student_dashboard.html')
    return render_template('student_dashboard.html')

# @app.route('/student_dashboard')
# def student_dashboard():
#     if 'user_email' not in session:
#         return redirect(url_for('user_login'))

#     conn = sqlite3.connect('counsellors.db')
#     cursor = conn.cursor()

#     # Get student_id
#     cursor.execute('SELECT id FROM users WHERE email = ?', (session['user_email'],))
#     student = cursor.fetchone()
#     student_id = student[0]

#     # Get latest scheduled call time
#     cursor.execute('''
#         SELECT scheduled_time FROM bookings
#         WHERE student_id = ? AND scheduled_time IS NOT NULL
#         ORDER BY scheduled_time DESC
#         LIMIT 1
#     ''', (student_id,))
#     row = cursor.fetchone()
#     conn.close()

#     show_message_button = False
#     if row:
#         from datetime import datetime, timedelta
#         scheduled_time = datetime.strptime(row[0], '%Y-%m-%d %H:%M')
#         now = datetime.now()
#         if scheduled_time <= now <= scheduled_time + timedelta(hours=24):
#             show_message_button = True

#     return render_template('student_dashboard.html', show_message_button=show_message_button)





@app.route('/counsellor_login',methods=['GET','POST'])
def counsellor_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('counsellors.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM counsellors WHERE email = ? AND password = ?', (email, password))
        counsellor = cursor.fetchone()
        conn.close()

        if counsellor:
            session['counsellor_id'] = counsellor[0]
            session['counsellor_name'] = counsellor[1]
            return redirect(url_for('counsellor_dashboard'))
        else:
            return render_template('counsellor_login.html', error='Invalid credentials!')
    
    return render_template('counsellor_login.html')
    # return render_template('counsellor_login.html')

# @app.route('/select_counsellor')
# def select_counsellor():
#     conn = sqlite3.connect('counsellors.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT id, name, email,specialization,bio,gender,experience FROM counsellors')

#     counsellors = cursor.fetchall()
#     print(counsellors)
    
    

#     cursor = conn.cursor()

#     # Get student_id
#     cursor.execute('SELECT id FROM users WHERE email = ?', (session['user_email'],))
#     student = cursor.fetchone()
#     student_id = student[0]

#     # Get latest scheduled call time
#     cursor.execute('''
#         SELECT scheduled_time FROM bookings
#         WHERE student_id = ? AND scheduled_time IS NOT NULL
#         ORDER BY scheduled_time DESC
#         LIMIT 1
#     ''', (student_id,))
#     row = cursor.fetchone()
#     conn.close()

#     show_message_button = False
#     if row:
#         from datetime import datetime, timedelta
#         scheduled_time = datetime.strptime(row[0], '%Y-%m-%d %H:%M')
#         now = datetime.now()
#         if scheduled_time <= now <= scheduled_time + timedelta(hours=24):
#             show_message_button = True
#     print("SHHHHHH",show_message_button)
#     return render_template('select_counsellor.html', counsellors=counsellors, show_message_button=show_message_button)


@app.route('/select_counsellor')
def select_counsellor():
    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()

    # Get all counsellors
    cursor.execute('SELECT id, name, email, specialization, bio, gender, experience FROM counsellors')
    counsellors = cursor.fetchall()

    # Get student_id
    cursor.execute('SELECT id FROM users WHERE email = ?', (session['user_email'],))
    student = cursor.fetchone()
    student_id = student[0]

    # Get current datetime
    from datetime import datetime, timedelta
    now = datetime.now()

    # Get all counsellor_ids with a valid session in the past 24 hours
    cursor.execute('''
        SELECT counsellor_id, scheduled_time FROM bookings
        WHERE student_id = ? AND scheduled_time IS NOT NULL
    ''', (student_id,))
    bookings = cursor.fetchall()

    active_counsellor_ids = set()
    for counsellor_id, scheduled_time in bookings:
        session_time = datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M')
        if session_time <= now <= session_time + timedelta(hours=24):
            active_counsellor_ids.add(counsellor_id)

    conn.close()

    return render_template('select_counsellor.html',
                           counsellors=counsellors,
                           active_counsellor_ids=active_counsellor_ids)


@app.route('/schedule_call/<int:booking_id>', methods=['GET', 'POST'])
def schedule_call_form(booking_id):
    conn = sqlite3.connect('counsellors.db')
    c = conn.cursor()

    # Get student email and name from booking
    c.execute("SELECT student_id,counsellor_id FROM bookings WHERE id = ?", (booking_id,))
    booking = c.fetchone()
    print(booking)
    
    c.execute("SELECT email FROM users WHERE id = ?",(booking[0],))
    studentemail = c.fetchone()

    c.execute("SELECT name FROM counsellors WHERE id = ?",(booking[1],))
    counsellorData = c.fetchone()
    print(counsellorData)
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        scheduled_datetime = f"{date} {time}"

        # Save the schedule info in DB (you may add a new column or new table)
        c.execute("UPDATE bookings SET scheduled_time = ? WHERE id = ?", (scheduled_datetime, booking_id))
        conn.commit()
        conn.close()

        # Send email to student
        send_email(
            to_email=studentemail[0],
            subject="Your Call Has Been Scheduled",
            body=f"Hi {studentemail[0]},\n\nYour call has been scheduled on {scheduled_datetime} by {counsellorData[0]}.\n\nThank you!"
        )

        flash("Call scheduled and student notified by email.", "success")
        return redirect(url_for('counsellor_dashboard'))

    return render_template('schedule_call.html', booking_id=booking_id, student=studentemail)



@app.route('/send_message/<int:counsellor_id>', methods=['GET', 'POST'])
def send_message(counsellor_id):
    if request.method == 'POST':
        student_email = session.get('user_email')
        conn = sqlite3.connect('counsellors.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE email = ?', (student_email,))
        student_id = cursor.fetchone()[0]
        message = request.form['message']
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO messages (student_id, counsellor_id, message, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (student_id, counsellor_id, message, timestamp))
        conn.commit()
        print("i am here!")
        conn.close()
        return redirect(url_for('select_counsellor'))
    
    return render_template('send_message.html', counsellor_id=counsellor_id)




@app.route('/counsellor_dashboard', methods=['GET', 'POST'])
def counsellor_dashboard():
    if 'counsellor_id' not in session:
        return redirect(url_for('counsellor_login'))

    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()

    # Fetch messages
    cursor.execute('''
        SELECT messages.id, users.name, messages.message, messages.reply
        FROM messages
        JOIN users ON messages.student_id = users.id
        WHERE messages.counsellor_id = ?
    ''', (session['counsellor_id'],))
    data = cursor.fetchall()
    print("fef",data)
    # Fetch bookings
    cursor.execute('''
        SELECT users.name, users.email, bookings.timestamp,bookings.id
        FROM bookings
        JOIN users ON bookings.student_id = users.id
        WHERE bookings.counsellor_id = ?
    ''', (session['counsellor_id'],))
    bookings = cursor.fetchall()
    print("BOKKING",bookings)
    # In counsellor_dashboard route, after fetching messages and bookings
    cursor.execute('SELECT bio FROM counsellors WHERE id = ?', (session['counsellor_id'],))
    bio_row = cursor.fetchone()
    bio = bio_row[0] if bio_row else ''
    print("Hi",bookings)
    conn.close()
    return render_template('counsellor_dashboard.html', messages=data, bookings=bookings,counsellor_bio=bio)



@app.route('/profile', methods=['GET'])
def counsellor_profile():
    if 'counsellor_id' not in session:
        return redirect(url_for('counsellor_login'))

    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()
    cursor.execute('SELECT bio, gender, experience FROM counsellors WHERE id = ?', (session['counsellor_id'],))
    row = cursor.fetchone()
    conn.close()

    bio = row[0] if row else ''
    gender = row[1] if row else ''
    experience = row[2] if row else ''

    return render_template('counsellor_profile.html', counsellor_bio=bio, gender=gender, experience=experience)



@app.route('/update_bio', methods=['POST'])
def update_bio():
    if 'counsellor_id' not in session:
        return redirect(url_for('counsellor_login'))

    new_bio = request.form['bio']
    gender = request.form['gender']
    experience = request.form['experience']

    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE counsellors SET bio = ?, gender = ?, experience = ?
        WHERE id = ?
    ''', (new_bio, gender, experience, session['counsellor_id']))
    conn.commit()
    conn.close()

    return redirect(url_for('counsellor_profile'))



@app.route('/reply_message/<int:message_id>', methods=['POST'])
def reply_message(message_id):
    reply = request.form['reply']
    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE messages SET reply = ? WHERE id = ?', (reply, message_id))
    conn.commit()
    conn.close()
    return redirect(url_for('counsellor_dashboard'))

@app.route('/book_session')
def book_session():
    return "<h2>Booking Page Coming Soon</h2>"




@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        conn = sqlite3.connect('counsellors.db')
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return render_template('signup.html', error='User already exists with this email.')

        # Insert new user
        cursor.execute('''
            INSERT INTO users (name, email, phone, password)
            VALUES (?, ?, ?, ?)
        ''', (name, email, phone, password))
        conn.commit()
        conn.close()

        return render_template('user_login.html', msg='Signup successful!')

    return render_template('signup.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
