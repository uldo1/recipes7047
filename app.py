# importing flask module fro
from flask import Flask, render_template, request, g
from flaskext.mysql import MySQL


mysql = MySQL()

# initializing a variable of Flask
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'feed_me'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


# decorating index function with the app.route with url as /login
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/aboutus')
def aboutus():
    return render_template("about_us.html")

@app.route('/contactus')
def contactus():
    return render_template("contact_us.html")

@app.route('/blog')
def blog():
    return render_template("blog.html")

@app.route('/loginpg', methods=['POST', 'GET'])
def loginpg():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            con = mysql.connect()
            cur = con.cursor()
            cur.execute('SELECT username FROM user WHERE email=%s AND password=%s',
                        (email, password))
            username = cur.fetchone()
            user = username[0]
            con.commit()

        except:
            con.rollback()

        finally:
            return render_template("login.html", username=user)
            con.close()

@app.route('/random')
def random():
        try:
            con = mysql.connect()
            cur = con.cursor()
            cur.execute('SELECT recipe_id,name FROM recipes ORDER BY RAND() LIMIT 1')
            data = cur.fetchone()
            recipe_id = data[0]
            recipe_nm = data[1]
            cur.execute('SELECT name,price FROM ingredients WHERE ingredient_id IN '
                        '(SELECT ingredient_id FROM relations WHERE recipe_id ='
                        '(%s))', recipe_id)
            ingredients = cur.fetchall()
            con.commit()
        except:
            con.rollback()

        finally:
            return render_template("show_receipe.html", pic_nm=recipe_id, recipe_name=recipe_nm,recipe_ingr=ingredients)
            con.close()

@app.route('/veggie')
def veggie():
        try:
            con = mysql.connect()
            cur = con.cursor()
            cur.execute('SELECT recipe_id,name FROM recipes WHERE category= "Vegeterian" ORDER BY RAND() LIMIT 1')
            data = cur.fetchone()
            recipe_id = data[0]
            recipe_nm = data[1]
            cur.execute('SELECT name,price FROM ingredients WHERE ingredient_id IN '
                        '(SELECT ingredient_id FROM relations WHERE recipe_id ='
                        '(%s))', recipe_id)
            ingredients = cur.fetchall()
            con.commit()
        except:
            con.rollback()

        finally:
            return render_template("show_receipe.html", pic_nm=recipe_id, recipe_name=recipe_nm,recipe_ingr=ingredients)
            con.close()

@app.route('/non_veggie')
def non_veggie():
        try:
            con = mysql.connect()
            cur = con.cursor()
            cur.execute('SELECT recipe_id,name FROM recipes WHERE category = "Non-Vegeterian" ORDER BY RAND() LIMIT 1')
            data = cur.fetchone()
            recipe_id = data[0]
            recipe_nm = data[1]
            cur.execute('SELECT name,price FROM ingredients WHERE ingredient_id IN '
                        '(SELECT ingredient_id FROM relations WHERE recipe_id ='
                        '(%s))', recipe_id)
            ingredients = cur.fetchall()
            con.commit()
        except:
            con.rollback()

        finally:
            return render_template("show_receipe.html", pic_nm=recipe_id, recipe_name=recipe_nm,recipe_ingr=ingredients)
            con.close()


if __name__ == "__main__":
    app.run()
