from flask import Blueprint, render_template, request, flash, jsonify
# from flask_login import login_required, current_user
# from . import db
import json
import psycopg2


def create_db_connection():
    conn = psycopg2.connect(
        host = "10.17.50.87",
        port = 5432,
        database = "group_12",
        user = "group_12",
        password = "ZzlQI7X4VqxdMJ" 
    )

    return conn

views = Blueprint('views', __name__)

bitval={'Documentary':0 ,  'Short':1 ,  'Animation':2, 'Comedy':3, 'Romance':4 ,'Sport':5, 'News':6,
 'Drama':7, 'Fantasy':8, 'Horror':9, 'Biography':10, 'Music':11, 'War':12, 'Crime':13, 'Western':14,
 'Family':15, 'Adventure':16, 'Action':17, 'History':18 ,'Mystery':19,  'Sci-Fi':20,
 'Musical':21, 'Thriller':22, 'Film-Noir':23, 'Talk-Show':24, 'Game-Show':25, 'Reality-TV':26,
 'Adult':27,'nan':28}

def genres_to_list(x):
    if x != None :
        result = 0
        for num in x:
            if num in bitval:
                # Use bitwise OR to set the corresponding bit to 1
                result |= 1 << bitval[num]
# Make sure the result is a 32-bit int
        result &= 0xFFFFFFFF
        return result
    else :
        result = 0
        result &= 0xFFFFFFFF
        return result


@views.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    if request.method == 'POST': 
        # note = request.form.get('note')#Gets the note from the HTML 
        note = "lol"
        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            # new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            # db.session.add(new_note) #adding the note to the database 
            # db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html")

@views.route('/movies', methods=['GET', 'POST'])
def movies_stuff():
    if request.method == 'POST': 
        conn = create_db_connection()
        cur = conn.cursor()
        # cur.execute("SELECT * FROM users u where u.email = '{}'".format(email))
        # data = cur.fetchall()

        data = {}
        for key, value in request.form.items():
            if value == '':
                data[key] = 'NULL'
            elif not value.isdigit():
                data[key] = '\'' + value + '\''
            else:
                data[key] = value

        substring_tolookfor = data['subsrting_tolookfor']
        num_votes_min = data['num_votes-min']
        num_votes_max = data['num_votes-max']
        release_date_min = data['release_date-min']
        release_date_max = data['release_date-max']
        runtime_min = data['runtime-min']
        runtime_max = data['runtime-max']
        moviemeter_min = data['moviemeter-min']
        moviemeter_max = data['moviemeter-max']
        genres = genres_to_list(request.form.getlist('genres'))

        query = open('website/pysql/movie-master.txt', 'r').read()
        formatted_query = query.format(
            t_title=substring_tolookfor,
            t_type='\'movie\'',
            srt_yr=release_date_min,
            end_yr=release_date_max,
            is_adlt='NULL',
            rn_time=runtime_max,
            t_genre_list=genres,
            cutOrIn='true'
        )
        cur.execute(formatted_query)
        ret = cur.fetchall()

        print(ret)
        
        # print(query)
             
    return render_template("movies.html")

@views.route('/people', methods=['GET', 'POST'])
def people():
    if request.method == 'POST': 
        person = request.form.get('p') 
    return render_template("people.html")

@views.route('/shows', methods=['GET', 'POST'])
def shows():
    if request.method == 'POST': 
        person = request.form.get('p') 
    return render_template("shows.html")

@views.route('/games', methods=['GET', 'POST'])
def games():
    if request.method == 'POST': 
        person = request.form.get('p')#Gets the note from the HTML 
    return render_template("games.html")


# @views.route('/delete-note', methods=['POST'])
# def delete_note():  
#     note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})
