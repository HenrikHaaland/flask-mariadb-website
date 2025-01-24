#imports 
from flask import Flask, render_template, redirect, request, session, jsonify
import mariadb
from flask_bcrypt import Bcrypt 
from flask_session import Session
import datetime


app = Flask(__name__)
bcrypt = Bcrypt(app) 

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



def connect_database():
    conn = mariadb.connect(
            host='localhost',
            port= 3306,
            user='root',
            password='beng123',
            database='bookstranslate')

    cur = conn.cursor()
    return cur, conn

@app.route('/', methods = ['POST', 'GET'])
def root():
    return render_template('login.html')

@app.route('/login_form_handler', methods = ['POST'])
def login_form_handler():
    if request.method == "POST":
        cursor, conn = connect_database()

        username = request.form["username"]
        password = request.form["password"]

        # Check if user exists
        query = "SELECT username, password FROM users WHERE username = %s LIMIT 1"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"error" : "noexist"})

        # If password is wrong
        hashed_password = result[1]
        is_valid = bcrypt.check_password_hash(hashed_password, password)
        if not is_valid:
            return jsonify({"error" : "wrong"})

        session["name"] = username

        # If everything went well, redirect
        return jsonify({"redirect" : 1})

@app.route('/createaccount', methods = ['POST', 'GET'])
def createacconut():
    if request.method == 'POST':
        

        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']

        cur, conn = connect_database()
        cur.execute("SELECT username FROM users WHERE username = ?", [username])
        result = cur.fetchone()
        if result:
            print("this username is already taken ")    
        
        

        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


        # Database connection
        cur.execute("INSERT INTO users(username, password, name, email) VALUES(?, ?, ?, ?)", (username, hashed_password, name, email))
        conn.commit()
        return redirect("/book")

        
        
    return render_template('createaccount.html') 


@app.route('/book', methods = ['POST', 'GET'])
def orderbooktranslation():
    if not session.get("name"):
        return redirect("/")
    if request.method == 'POST':
        name = request.form['name']
        user_id = 1
        book_name = request.form['book_name']
        author = request.form['author']
        og_language = request.form['og_language']
        new_language = request.form['new_language']
        description = request.form['description']
        created = datetime.datetime.now()
        modified = datetime.datetime.now()

        cur, conn = connect_database()

        cur.execute("INSERT INTO bookorder(name, user_id, book_name, author, og_language, new_language, description, created, modified) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, user_id, book_name, author, og_language, new_language, description, created, modified))
        conn.commit()
        
    
    name = session.get("name")  

    return render_template('book.html', session=name)





if __name__ == '__main__':
    app.run(debug=True)
