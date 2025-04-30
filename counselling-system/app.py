from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import sqlite3
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management


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
        specialization TEXT NOT NULL
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

# # Insert fixed counsellors (only run once)
#     cursor.execute("SELECT COUNT(*) FROM counsellors")
#     if cursor.fetchone()[0] == 0:
#             counsellor_data = [
#         ("Alice", "alice@counsel.com", "123", "Academic"),
#         ("Bob", "bob@counsel.com", "123", "Career"),
#         ("Carol", "carol@counsel.com", "123", "Personal"),
#         ("Dave", "dave@counsel.com", "123", "Health"),
#         ("Eve", "eve@counsel.com", "123", "Financial")
#     ]
#     cursor.executemany("INSERT INTO counsellors (name, email, password, specialization) VALUES (?, ?, ?, ?)", counsellor_data)



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

    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, email, phone FROM users')
    students = cursor.fetchall()
    cursor.execute('SELECT name, email, specialization FROM counsellors')
    counsellors = cursor.fetchall()
    conn.close()

    return render_template('admin_dashboard.html', students=students, counsellors=counsellors)


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
        use = 'user_email' in session
        print("Hi",use)
        return redirect(url_for('user_login'))
        #return render_template('student_dashboard.html')
    return render_template('student_dashboard.html')




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

@app.route('/select_counsellor')
def select_counsellor():
    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, specialization FROM counsellors')
    counsellors = cursor.fetchall()
    conn.close()
    return render_template('select_counsellor.html', counsellors=counsellors)


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
    cursor.execute('''
        SELECT messages.id, users.name, messages.message, messages.reply
        FROM messages
        JOIN users ON messages.student_id = users.id
        WHERE messages.counsellor_id = ?
    ''', (session['counsellor_id'],))
    data = cursor.fetchall()
    conn.close()
    return render_template('counsellor_dashboard.html', messages=data)


@app.route('/reply_message/<int:message_id>', methods=['POST'])
def reply_message(message_id):
    reply = request.form['reply']
    conn = sqlite3.connect('counsellors.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE messages SET reply = ? WHERE id = ?', (reply, message_id))
    conn.commit()
    conn.close()
    return redirect(url_for('counsellor_dashboard'))


@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/signup',methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         password = request.form['password']
#         print(name,email)
#         conn = sqlite3.connect('counsellors.db')
#         cursor = conn.cursor()
#         cursor.execute('''
#             INSERT INTO users (name, email, phone, password)
#             VALUES (?, ?, ?, ?)
#         ''', (name, email, phone, password))
#         conn.commit()
#         conn.close()
#         return render_template('user_login.html',msg='Signup successful!')
#     return render_template('signup.html')


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
