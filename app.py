# importing flask module fro
from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import requests  # for API example
import urllib.parse  # for API example

mysql = MySQL()

# initializing a variable of Flask
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'feedme'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# decorating index function with the app.route with url as /login
@app.route('/')
def home():
    return render_template("home.html")


@app.route('/loginpg', methods=['POST', 'GET'])
def loginpg():
    if request.method == 'POST':
        try:
            email_address = request.form['email']
            password = request.form['password']
            con = mysql.connect()
            cur = con.cursor()
            cur.execute('SELECT username, email FROM users WHERE email=%s AND password=%s',
                        (email_address, password))
            rows = cur.fetchall()
            con.commit()

        except:
            con.rollback()

        finally:
            return render_template("login.html")
            con.close()

if __name__ == "__main__":
    app.run()