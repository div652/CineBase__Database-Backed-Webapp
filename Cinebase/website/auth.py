# <<<<<<< HEAD
from flask import Blueprint, render_template, request, flash, redirect, url_for, g,session
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import login_user, login_required, logout_user
import psycopg2

curr_user = "guest@nomail.com"
Name_of_user = "Guest User"

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host = "10.17.50.87",
            port = 5432,
            database = "group_12",
            user = "group_12",
            password = "ZzlQI7X4VqxdMJ" 
        )
    return g.db

def create_db_connection():
    conn = psycopg2.connect(
        host = "10.17.50.87",
        port = 5432,
        database = "group_12",
        user = "group_12",
        password = "ZzlQI7X4VqxdMJ" 
    )
    return conn

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    global curr_user,Name_of_user
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = create_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users u where u.emailid = '{}'".format(email))
        data = cur.fetchall()
        
        
        if len(data) == 1:
            if check_password_hash(data[0][0], password):
                flash('Logged in successfully!', category='success')
                session['logged_in'] = True
                curr_user = email
                session['username'] =  data[0][1]
                print("new name of use is now",data[0][1])
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email is not registered here. Please signup first.', category='error')

    return render_template("login.html",user=curr_user,name_of_user=Name_of_user)


@auth.route('/logout')
# @login_required
def logout():
    global curr_user,Name_of_user
    curr_user = "Guest"
    session['username'] ="Guest User"
    session['logged_in'] = False
    flash('Logged out !', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    global curr_user,Name_of_user
    if request.method == 'POST':

        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        dob = request.form.get('dob')
        city = request.form.get('city')

        conn = create_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users u where u.emailid = '{}'".format(email))
        data = cur.fetchall()
        
        if len(data) > 0:
            flash('User already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            hsh = generate_password_hash(password1, method='sha256')
            cmd = "INSERT INTO users (password, username, emailid, birthdate, location) VALUES ('{}', '{}', '{}', '{}', '{}');".format(hsh, first_name, email, dob, city)
            cur.execute(cmd)
            conn.commit()
            curr_user = email
            Name_of_user = first_name
            flash('Account created!', category='success')

        cur.close()
        conn.close()
        return redirect(url_for('views.home'))

    return render_template("sign_up.html",user=curr_user,name_of_user=Name_of_user)
# =======
# from flask import Blueprint, render_template, request, flash, redirect, url_for, g,session
# from werkzeug.security import generate_password_hash, check_password_hash
# # from flask_login import login_user, login_required, logout_user
# import psycopg2

# curr_user = "guest@nomail.com"
# Name_of_user = "Guest User"

# # def get_db():
# #     if 'db' not in g:
# #         g.db = psycopg2.connect(
# #             host = "10.17.50.87",
# #             port = 5432,
# #             database = "group_12",
# #             user = "group_12",
# #             password = "ZzlQI7X4VqxdMJ" 
# #         )
# #     return g.db

# def create_db_connection():
#     conn = psycopg2.connect(
#         host = "10.17.50.87",
#         port = 5432,
#         database = "group_12",
#         user = "group_12",
#         password = "ZzlQI7X4VqxdMJ" 
#     )
#     return conn

# auth = Blueprint('auth', __name__)


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     global curr_user
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         conn = create_db_connection()
#         cur = conn.cursor()

#         cur.execute("SELECT * FROM users u where u.emailid = '{}'".format(email))
#         data = cur.fetchall()
        
        
#         if len(data) == 1:
#             if check_password_hash(data[0][0], password):
#                 flash('Logged in successfully!', category='success')
#                 session['logged_in'] = True
#                 curr_user = email
#                 return redirect(url_for('views.home'))
#             else:
#                 flash('Incorrect password, try again.', category='error')
#         else:
#             flash('Email does not exist.', category='error')

#     return render_template("login.html",user=curr_user,name_of_user=Name_of_user)


# @auth.route('/logout')
# # @login_required
# def logout():
#     global curr_user
#     curr_user = "Guest"
#     Name_of_user="Guest User"
#     session['logged_in'] = False
#     flash('Logged out !', category='success')
#     return redirect(url_for('auth.login'))


# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     global curr_user,Name_of_user
#     if request.method == 'POST':

#         email = request.form.get('email')
#         first_name = request.form.get('firstName')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')
#         dob = request.form.get('dob')
#         city = request.form.get('city')

#         conn = create_db_connection()
#         cur = conn.cursor()

#         cur.execute("SELECT * FROM users u where u.emailid = '{}'".format(email))
#         data = cur.fetchall()
        
#         if len(data) > 0:
#             flash('Email already exists.', category='error')
#         elif len(email) < 4:
#             flash('Email must be greater than 3 characters.', category='error')
#         elif len(first_name) < 2:
#             flash('First name must be greater than 1 character.', category='error')
#         elif password1 != password2:
#             flash('Passwords don\'t match.', category='error')
#         elif len(password1) < 7:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
#             hsh = generate_password_hash(password1, method='sha256')
#             cmd = "INSERT INTO users (emailid, password, username, birthdate) VALUES ('{}', '{}', '{}', '{}');".format(email, hsh, first_name, dob, city)
#             cur.execute(cmd)
#             conn.commit()
#             curr_user = email
#             Name_of_user = first_name
#             flash('Account created!', category='success')

#         cur.close()
#         conn.close()
#         return redirect(url_for('views.home'))

#     return render_template("sign_up.html",user=curr_user,name_of_user=Name_of_user)
# >>>>>>> 5dd1808641fde92b365c31f2690804b980e80100
