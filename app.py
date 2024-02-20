from flask import Flask, render_template, request, redirect, url_for, flash
import time
from werkzeug.security import generate_password_hash, check_password_hash
from MySQL import User ,retrieve_users_from_mysql
import os

app = Flask(__name__)
SECRET_KEY =  os.urandom(24)
app.secret_key = SECRET_KEY

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login.html')
def index():
    signin_condition = True
    return render_template('login.html', condition = signin_condition)

@app.route('/SignIn', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    hashPassword = generate_password_hash(password, method='pbkdf2')

    user = retrieve_users_from_mysql(email)
    if user == None:
        flash('No User Found')
        signin_condition = True
        render_template('login.html', condition = signin_condition)
        time.sleep(3)
        return redirect(url_for('home'))
    elif user.password == hashPassword:
        if check_password_hash(user.password, password):
            if user.isAdmin:
                flash('Admin SignIn Successfull')
            else:
                flash('SignIn Successfull')
            time.sleep(3)
            return redirect(url_for('home'))
    else:
        flash('Incorect password')
        # time.sleep(3)
        return redirect(url_for('index'))

# @app.route('/SignUp', methods=['POST'])
# def signup():
#     username = request.form['username']
#     password = request.form['password']

#     signup_data[username] = password
#     return redirect(url_for('index'))

# @app.route('/success')
# def success():
#     return 'Login successful!'

if __name__ == '__main__':
    app.run(debug=True)
