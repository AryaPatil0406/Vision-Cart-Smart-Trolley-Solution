from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import subprocess
import pandas as pd

app = Flask(__name__)

# Path to the SQLite database
DB_PATH = 'users.db'

# Initialize the SQLite database (create the database and users table if not exists)
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT)''')
        conn.commit()
        conn.close()

# Call init_db when the app starts to ensure the database is created
init_db()

# Create a signup and login page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        password = request.form['password']
        
        if action == 'Login':
            # Check if username and password match in the database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return redirect(url_for('dashboard'))
            else:
                return "Invalid login credentials. Try again."
        
        elif action == 'Signup':
            # Check if the username already exists
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                conn.close()
                return "Username already exists. Try a different one."
            else:
                # Insert new user into the database
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                conn.close()
                return "Signup successful. You can now log in."
    
    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Route for live webcam
@app.route('/live-webcam')
def live_webcam():
    # Command to run for live webcam
    command = [
        "python",
        "D:\\vision cart\\Mini_Project_2\\YOLOv8-DeepSORT-Object-Tracking\\ultralytics\\yolo\\v8\\detect\\predict.py",
        "model=best.pt",
        "source=0",
        "show=True"
    ]
    subprocess.run(command)
    return redirect(url_for('show_report'))

# Route for video upload
@app.route('/upload-video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        video = request.files['video']
        video_path = os.path.join('uploads', video.filename)
        
        # Save the uploaded video
        os.makedirs('uploads', exist_ok=True)
        video.save(video_path)
        
        # Command to run for uploaded video
        command = [
            "python",
            "D:\\vision cart\\Mini_Project_2\\YOLOv8-DeepSORT-Object-Tracking\\ultralytics\\yolo\\v8\\detect\\predict.py",
            f"model=best.pt",
            f"source={video_path}",
            "show=True"
        ]
        subprocess.run(command)
        return redirect(url_for('show_report'))
    return render_template('upload_video.html')

# Route to show the bill (Excel file)
@app.route('/show-report')
def show_report():
    excel_path = "D:\\vision cart\\Mini_Project_2\\YOLOv8-DeepSORT-Object-Tracking\\ultralytics\\yolo\\v8\\detect\\counting_report.xlsx"
    
    if os.path.exists(excel_path):
        try:
            import pandas as pd
            df = pd.read_excel(excel_path)
            return render_template('report.html', tables=[df.to_html(classes='table')])
        except Exception as e:
            return f"Error reading the Excel file: {e}"
    else:
        return f"No report available. Expected file path: {excel_path}"

# Route to the "Pay Bill" page
@app.route('/pay', methods=['GET', 'POST'])
def pay_bill():
    if request.method == 'POST':
        # Handle the payment confirmation form
        name = request.form['name']
        amount = request.form['amount']
        
        # You can add logic here to process the payment (e.g., save payment info, connect to a payment gateway)
        return render_template('payment_confirmation.html', name=name, amount=amount)
    
    return render_template('pay.html')

# Route to display payment confirmation
@app.route('/payment-confirmation', methods=['POST'])
def payment_confirmation():
    name = request.form['name']
    amount = request.form['amount']
    
    # Display a success message
    return render_template('payment_confirmation.html', name=name, amount=amount)

if __name__ == '__main__':
    app.run(debug=True)
