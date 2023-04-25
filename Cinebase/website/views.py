from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
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
        movie = request.form.get('movie')#Gets the note from the HTML 
    return render_template("movies.html")

@views.route('/people', methods=['GET', 'POST'])
def people():
    if request.method == 'POST': 
        person = request.form.get('p')#Gets the note from the HTML 
    return render_template("people.html")


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
