from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import psycopg2


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
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # login_user(email, remember=True)
        # user = User.query.filter_by(email=email).first()
        # if user:
        #     if check_password_hash(user.password, password):
        #         flash('Logged in successfully!', category='success')
        #         login_user(user, remember=True)
        #         return redirect(url_for('views.home'))
        #     else:
        #         flash('Incorrect password, try again.', category='error')
        # else:
        #     flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
# @login_required
def logout():
    # logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':

        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        dob = request.form.get('dob')
        city = request.form.get('city')

        conn = create_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users u where u.email = '{}'".format(email))
        data = cur.fetchall()
        
        if len(data) > 0:
            flash('Email already exists.', category='error')
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
            cmd = "INSERT INTO users (userid, password, username, email, birthdate) VALUES ({}, '{}', '{}', '{}', '{}');".format(1, hsh, first_name, email, dob)
            cur.execute(cmd)
            conn.commit()
            flash('Account created!', category='success')

        cur.close()
        conn.close()
        return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
