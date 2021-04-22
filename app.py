# app

from flask import Flask,render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL

from sqlhelpers import *
from forms import *
# from password import _mysql_password

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crypto'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route("/register", methods = ['GET','POST'])
def register():
    form = RegisterForm(request.form)
    users = Table("user", "name", "email", "username", "password")
    if request.method == 'POST' and form.validate():
        return render_template('register.html', form = form)
    return render_template('register.html', form = form)

@app.route("/")
def index():
    # users = Table("user", "name", "email", "username", "password")
    # users.insert("An1", "ghostkey.war@gmail.com", "red2374", "hash")
    # users.drop()
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 's123'
    app.run(debug= True)
