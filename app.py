from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = "130>me"

def getConnection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/resume')
def food():
    return render_template("resume.html")

@app.route('/work')
def train():
    return render_template("work.html")

@app.route('/personal_traning')
def train_list():
    return render_template("personal_training.html")

@app.route('/signup', methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        login =request.form['login']
        password =request.form['password']
        confirm_password =request.form['confirm_password']
        if password!= confirm_password:
            print("323")
            return redirect(url_for('signup'))#переадресація на url_for адресу
        connection = getConnection()
        user = connection.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password)).fetchone()
        if user:
            return redirect(url_for('signup'))#переадресація на url_for адресу
        if  not user:
            connection.execute("INSERT INTO users (login, password) VALUES(?,?)", (login, password))
            connection.commit()
            connection.close()
            return redirect(url_for('login'))#переадресація на url_for адресу
    return render_template('signup.html')

@app.route('/login')
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        conn = getConnection()
        user = conn.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
        if user:
            session['login'] = user['login']
            return redirect(url_for('work'))
        else:
            flash("Логін або пароль не вірний")
            return redirect(url_for('login'))
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run()

