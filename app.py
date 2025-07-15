from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_type = request.form['user_type']
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    if user_type == 'admin':
        user = conn.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password)).fetchone()
        if user:
            session['admin'] = username
            return redirect('/admin')
    else:
        user = conn.execute('SELECT * FROM students WHERE student_id = ? AND password = ?', (username, password)).fetchone()
        if user:
            session['student'] = username
            return redirect('/student')
    conn.close()
    return redirect('/')

@app.route('/admin')
def admin_dashboard():
    if 'admin' in session:
        conn = get_db_connection()
        students = conn.execute('SELECT * FROM students').fetchall()
        conn.close()
        return render_template('admin.html', students=students)
    return redirect('/')

@app.route('/student')
def student_dashboard():
    if 'student' in session:
        conn = get_db_connection()
        student = conn.execute('SELECT * FROM students WHERE student_id = ?', (session['student'],)).fetchone()
        conn.close()
        return render_template('student.html', student=student)
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)