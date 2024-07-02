from flask import Flask, request, redirect, render_template
import hashlib
import sqlite3

app = Flask(__name__)

# Function to initialize the database
def init_db():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS urls
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       long_url TEXT NOT NULL,
                       short_id TEXT NOT NULL UNIQUE)''')
    conn.commit()  # Save changes
    conn.close()   # Close the connection

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('urls.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

# Function to generate a short ID for the URL using MD5 hash
def generate_short_id(long_url):
    return hashlib.md5(long_url.encode()).hexdigest()[:6]

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']  # Get the long URL from the form
        short_id = generate_short_id(long_url)  # Generate a short ID
        
        conn = get_db_connection()
        cursor = conn.cursor()
        # Insert the long URL and short ID into the database
        cursor.execute('INSERT INTO urls (long_url, short_id) VALUES (?, ?)', (long_url, short_id))
        conn.commit()  # Save changes
        conn.close()   # Close the connection

        short_url = request.host_url + short_id  # Construct the short URL
        return render_template('index.html', short_url=short_url)  # Display the short URL
    return render_template('index.html')  # Render the home page

# Route to handle the redirection from short URL to long URL
@app.route('/<short_id>')
def redirect_to_long_url(short_id):
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
