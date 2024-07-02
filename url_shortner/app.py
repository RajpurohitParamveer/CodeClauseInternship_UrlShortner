from flask import Flask, request, redirect, render_template
import hashlib
import sqlite3
import threading
import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Lock for database operations to avoid "database is locked" errors
db_lock = threading.Lock()

# Expiry time for URLs in days
URL_EXPIRY_DAYS = 7

# Function to initialize the database
def init_db():
    with db_lock:
        conn = sqlite3.connect('urls.db', check_same_thread=False, timeout=10)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS urls
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           long_url TEXT NOT NULL,
                           short_id TEXT NOT NULL UNIQUE,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('urls.db', check_same_thread=False, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

# Function to generate a short ID for the URL using MD5 hash
def generate_short_id(long_url):
    return hashlib.md5(long_url.encode()).hexdigest()[:6]

# Function to delete expired URLs
def delete_expired_urls():
    with db_lock:
        conn = get_db_connection()
        cursor = conn.cursor()
        expiration_date = datetime.datetime.now() - datetime.timedelta(days=URL_EXPIRY_DAYS)
        cursor.execute('DELETE FROM urls WHERE created_at < ?', (expiration_date,))
        conn.commit()
        conn.close()

# Schedule the deletion of expired URLs
scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_expired_urls, trigger="interval", days=1)
scheduler.start()

# Ensure the scheduler shuts down properly
atexit.register(lambda: scheduler.shutdown())

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']  # Get the long URL from the form
        short_id = generate_short_id(long_url)  # Generate a short ID
        
        with db_lock:
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                # Insert the long URL and short ID into the database
                cursor.execute('INSERT INTO urls (long_url, short_id) VALUES (?, ?)', (long_url, short_id))
                conn.commit()  # Save changes
            except sqlite3.IntegrityError:
                # Handle duplicate short_id
                return render_template('index.html', error="This URL has already been shortened.")
            finally:
                conn.close()   # Close the connection

        short_url = request.host_url + short_id  # Construct the short URL
        return render_template('index.html', short_url=short_url)  # Display the short URL
    return render_template('index.html')  # Render the home page

# Route to handle the redirection from short URL to long URL
@app.route('/<short_id>')
def redirect_to_long_url(short_id):
    with db_lock:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Query the database for the long URL corresponding to the short ID
        cursor.execute('SELECT long_url FROM urls WHERE short_id = ?', (short_id,))
        result = cursor.fetchone()
        conn.close()  # Close the connection
        if result:
            return redirect(result['long_url'])  # Redirect to the long URL
        else:
            return 'URL not found', 404  # Return 404 if short ID is not found

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)  # Run the Flask app in debug mode
