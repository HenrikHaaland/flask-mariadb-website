from flask import Flask, render_template, redirect, url_for, request
import mariadb
from flask_bcrypt import Bcrypt 


app = Flask(__name__)
bcrypt = Bcrypt(app) 


def connect_database():
    conn = mariadb.connect(
            host='localhost',
            port= 3306,
            user='root',
            password='beng123',
            database='bookstranslate')

    cur = conn.cursor()
    return cur, conn

@app.route('/')
def root():
    return render_template('login.html')

@app.route('/createaccount', methods = ['POST', 'GET'])
def createacconut():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']

        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


        # Database connection
        cur, conn = connect_database()
        cur.execute("INSERT INTO users(username, password, name, email) VALUES(?, ?, ?, ?)", (username, hashed_password, name, email))
        conn.commit()
        
        
    return render_template('createaccount.html')





if __name__ == '__main__':
    app.run(debug=True)
