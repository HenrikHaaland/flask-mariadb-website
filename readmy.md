import sqlite3

def start_db():
    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    username TEXT
                   )''')
    
    cursor.execute('''
        INSERT INTO users (name, email, password, username)
        VALUES ('John Doe', 'john@example.com', 'password123', 'johndoe')
    ''')

    conn.commit()
    conn.close()

    print("Database and table created successfully.")

start_db()


{% extends 'base.html' %}
{% block body %}
<h1>hei</h1>
<style>body {background-color: green;}</style>
{% endblock %}  

{% extends 'base.html' %}
{% block body %}
<h1>hade</h1>
<style>body {background-color: red;}</style>
{% endblock %}


{% block body %}
{% endblock %}