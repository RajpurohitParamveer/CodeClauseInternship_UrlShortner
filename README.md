In this project, I developed a URL shortener web application using Python's Flask framework and SQLite database. The application takes a long URL as input and generates a shortened version, which can be used to redirect to the original URL. This project helped me gain practical experience in web development, database management, and URL manipulation.

Libraries Used:
1.	Flask: A lightweight web framework for building web applications in Python. Flask was used to create the web interface and handle HTTP requests and responses.
2.	SQLite: A lightweight, disk-based database that doesn't require a separate server process. SQLite was used to store the mapping between long URLs and their corresponding short URLs.
3.	hashlib: A Python library that provides secure hash functions. It was used to generate unique short identifiers for the URLs.

Project Structure:
 url_shortener/
├── app.py
├── templates/
│   └── index.html
└── static/
    └── styles.css

Explanation of Key Components:
1.	app.py:
o	Flask Application Setup: Set up the Flask application and defined routes for handling user requests.
o	Database Initialization: Created a function to initialize the SQLite database and create the urls table if it doesn't exist.
o	URL Shortening Logic: Implemented functions to generate short IDs using the MD5 hash of the long URL and to store and retrieve URL mappings from the database.
o	Web Routes: Defined routes for the home page, handling URL submissions, and redirecting short URLs to their corresponding long URLs.

2.  templates/index.html:
•	HTML template for the web interface, providing a form to input long URLs and displaying the shortened URLs.

3.  static/styles.css:
•	CSS file for basic styling of the web interface.

What I Learned:
1.	Web Development with Flask: Gained hands-on experience in setting up a Flask application, defining routes, and rendering templates.
2.	Database Management with SQLite: Learned how to interact with SQLite databases in Python, including creating tables, inserting data, and querying data.
3.	URL Shortening Logic: Understood the principles behind generating unique short identifiers for URLs and mapping them to the original long URLs.
4.	Form Handling and Redirection: Learned how to handle form submissions in Flask and redirect users to different URLs based on input.

This project provided valuable insights into building web applications, handling user inputs, and managing data efficiently using databases.
