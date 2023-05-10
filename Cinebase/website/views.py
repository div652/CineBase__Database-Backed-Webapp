
from flask import Blueprint, render_template, request, flash, jsonify, session,redirect
# from flask_login import login_required, current_user
# from . import db
import json
import psycopg2
from .auth import curr_user
import requests
from bs4 import BeautifulSoup

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

    return render_template("home.html",user=curr_user,name_of_user=session.get('username') )

@views.route('/movies', methods=['GET', 'POST'])
def movies_stuff():
    if not session.get('logged_in'):
        flash('You must login to continue to this page', category='error')
        return render_template("home.html",user=curr_user,name_of_user=session.get('username') )
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
        # print(formatted_query)
        ret = cur.fetchall()
        new_ret = [(x[0], x[2],x[5]) for x in ret]
        
        # print(query)     
        return render_template("outputMovies.html",user=curr_user,name_of_user=session.get('username') ,tuples=new_ret)
    
    return render_template("movies.html",user=curr_user,name_of_user=session.get('username') )

@views.route('/people', methods=['GET', 'POST'])
def people():
    if not session.get('logged_in'):
        flash('You must login to continue to this page', category='error')
        return render_template("home.html",user=curr_user,name_of_user=session.get('username') )
        
    if request.method == 'POST': 
        person = request.form.get('p')#Gets the note from the HTML 
    return render_template("people.html",user=curr_user,name_of_user=session.get('username') )

@views.route('/shows', methods=['GET', 'POST'])
def shows():
    if not session.get('logged_in'):
        flash('You must login to continue to this page', category='error')
        return render_template("home.html",user=curr_user,name_of_user=session.get('username') )
    if request.method == 'POST': 
        person = request.form.get('p')#Gets the note from the HTML 
    return render_template("shows.html",user=curr_user,name_of_user=session.get('username') )

@views.route('/games', methods=['GET', 'POST'])
def games():
    if not session.get('logged_in'):
        flash('You must login to continue to this page', category='error')
        return render_template("home.html",user=curr_user,name_of_user=session.get('username') )
    if request.method == 'POST': 
        person = request.form.get('p')#Gets the note from the HTML 
    return render_template("games.html",user=curr_user,name_of_user=session.get('username') )

@views.route('/quickLinks', methods=['GET', 'POST'])
def quickLinks():
    link = request.args.get('link')
    # Here you can use the value of `link` to determine what output to show
    return render_template('quickLinks.html', link=link,user=curr_user,name_of_user=session.get('username') )

@views.route('/movie_info', methods=['GET', 'POST'])
def movie_info():
    titleid = request.args.get('titleid')
    user_email = session.get('curr_user')
    moviename = request.args.get('moviename')
    if not session.get('logged_in'):
        flash('You must login to continue to this page', category='error')
        return render_template("home.html",user=curr_user,name_of_user=session.get('username') )
    # if request.method == 'POST': 
        # person = request.form.get('p')#Gets the note from the HTML
    
    if request.method=='POST':
        conn = create_db_connection()
        cur = conn.cursor()
        print(request.form)
        if 'update_submission' in request.form:
            query = open('website/pysql/update_rating.txt','r').read()
            
            formatted_query=query.format(
                email_id = '\''+user_email+'\'', 
                title_id = '\''+titleid+'\'',
                rating_num = request.form.get("rating_update")
                )
            print("UPDATING A RATING")
            cur.execute(formatted_query)
            conn.commit()
            
            flash('Rating Updated successfully!', category='success')
            return redirect(f"/movie_info?titleid={titleid}&moviename={moviename}")
            
            
            
        else:
            query = open('website/pysql/insert_rating.txt','r').read()
            
            formatted_query=query.format(
                email_id = '\''+user_email+'\'', 
                title_id = '\''+titleid+'\'',
                rating_num = request.form.get("rating_insert")
                )
            print("formatted query executed is ",formatted_query)
            cur.execute(formatted_query)
            conn.commit()
            flash('Rated movie successfully!', category='success')
            return redirect(f"/movie_info?titleid={titleid}&moviename={moviename}")

    conn = create_db_connection()
    cur = conn.cursor()
    
    query = "obama"  # the search query you want to make
    url = f"https://www.google.com/search?q={query}&amp;tbm=isch"  # the URL of the search result page
    
    print("the url searched is ",url)
    response = requests.get(url)  # make a GET request to the URL
    soup = BeautifulSoup(response.text, "html.parser")  # parse the HTML content with BeautifulSoup
    
    # find the first image link by searching for the appropriate tag and attribute
    img_tag = soup.find("img", {"class": "yWs4tf"})
    
    if img_tag is not None:
        img_link = img_tag.get("src")
        print(img_link)  # print the first image link
    else:
        print("No image found on the page.")

    user_has_rated=False
    query = open('website/pysql/check-rated.txt','r').read()
    print("USER EMAIL IS :",user_email)
    formatted_query=query.format(
        email_id = '\''+user_email+'\'', 
        title_id = '\''+titleid+'\''
        
    )
    cur.execute(formatted_query)
    past_rating=0
    ret=cur.fetchall()
    print(type(ret))
    print(len(ret))
    if(not(len(ret)==0)):
        user_has_rated=True
        print("Bazinga")
        past_rating=ret[0][2]
    
    
    print("ret is ",ret, " and past_rating is ",past_rating)
    query = open('website/pysql/movie-info.txt', 'r').read()
    formatted_query = query.format(
        movie_tid='\''+titleid+'\'',
    )
    
    cur.execute(formatted_query)
    # print(formatted_query)
    # if ret[0][2] is None:
    #     ret[0][2] = "Not Released Yet"
    print("When searching for movie info the query id was ",formatted_query)
    
    ret = cur.fetchall()
    if(len(ret)==0):
        flash('Movie has not released yet', category='error')
        return redirect(request.referrer or '/')
    else:    
        return render_template("movie_info.html",user=curr_user,name_of_user=session.get('username') , movie_data=ret,movie_name=moviename,user_has_rated=user_has_rated,past_rating=past_rating)
        
        

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

