
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
bitval={'documentary':0 ,  'short':1 ,  'animation':2, 'comedy':3, 'romance':4 ,'sport':5, 'news':6,
 'drama':7, 'fantasy':8, 'horror':9, 'biography':10, 'music':11, 'war':12, 'crime':13, 'western':14,
 'family':15, 'adventure':16, 'action':17, 'history':18 ,'mystery':19,  'sci_fi':20,
 'musical':21, 'thriller':22, 'film_noir':23, 'talk_show':24, 'game_show':25, 'reality_tv':26,
 'adult':27,'nan':28}

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
        genres = genres_to_list(request.form.getlist('genres'))
        cut_or_in = request.form[('flexRadioDefault1')]
        print(cut_or_in)
        query = open('website/pysql/movie-master.txt', 'r').read()
        isAdult='false'
    
        if(session.get('isAdult')):
            print("this person is ",session['isAdult'])
            if(session['isAdult'] =='true'):
                isAdult='NULL'
        print(isAdult)
        formatted_query = query.format(
            t_title=substring_tolookfor,
            t_type='\'movie\'',
            srt_yr=release_date_min,
            end_yr=release_date_max,
            is_adlt=isAdult,
            rn_time_min=runtime_min,
            rn_time_max=runtime_max,
            t_genre_list=genres,
            cutOrIn=cut_or_in
        )
        cur.execute(formatted_query)
        print(formatted_query)
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
        conn = create_db_connection()
        cur = conn.cursor()
        # data = cur.fetchall()

        data = {}
        for key, value in request.form.items():
            if value == '':
                data[key] = 'NULL'
            elif not value.isdigit():
                data[key] = '\'' + value + '\''
            else:
                data[key] = value

        celeb_name = data['person_name_substr']
        title_name = data['title_name_substr']
        colab_name = data['colab_name_substr']
        # release_date_min = data['release_date-min']
        # release_date_max = data['release_date-max']
        # runtime_min = data['runtime-min']
        # runtime_max = data['runtime-max']
        # moviemeter_min = data['moviemeter-min']
        # moviemeter_max = data['moviemeter-max']
        genres = genres_to_list(request.form.getlist('genres'))

        if title_name!='NULL':
            query = open('website/pysql/person-title.txt', 'r').read()
            formatted_query = query.format(
                u_celeb=celeb_name,
                u_title=title_name
            )
            cur.execute(formatted_query)
            print(formatted_query)
            ret = cur.fetchall()
            new_ret = [(x[0], x[1], x[2], x[3]) for x in ret]
            
            # print(query)     
            return render_template("outputPeopleMovies.html",user=curr_user,name_of_user=session.get('username') ,tuples=new_ret)

        elif colab_name!='NULL':
            query = open('website/pysql/person-colab.txt', 'r').read()
            formatted_query = query.format(
                u_celeb=celeb_name,
                u_colab=colab_name
            )
            cur.execute(formatted_query)
            print(formatted_query)
            ret = cur.fetchall()
            new_ret = [(x[0], x[1], x[2], x[3]) for x in ret]
            
            # print(query)     
            return render_template("outputPeopleMovies.html",user=curr_user,name_of_user=session.get('username') ,tuples=new_ret)
        
        elif genres!='NULL':
            query = open('website/pysql/person-genre.txt', 'r').read()
            formatted_query = query.format(
                u_celeb=celeb_name,
                u_genres=genres
            )
            print(formatted_query)
            cur.execute(formatted_query)
            ret = cur.fetchall()
            new_ret = [(x[0], x[1]) for x in ret]
            
            # print(query)     
            return render_template("outputPeople.html",user=curr_user,name_of_user=session.get('username') ,tuples=new_ret)

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
    conn = create_db_connection()
    cur = conn.cursor()
    print(link)
    if link=='1':
        query = open('website/pysql/mp-movies-alltime.txt', 'r').read()
        formatted_query = query.format()
        cur.execute(formatted_query)
        # print(formatted_query)
        ret = cur.fetchall()
        new_ret = [(x[0], x[2], x[5], x[9]) for x in ret]
        return render_template('outputMoviesRatings.html', user=curr_user,name_of_user=session.get('username'), tuples=new_ret)

    elif link=='2':
        query = "select * from title where startYear>=2023 and titleType='movie';"
        formatted_query = query.format()
        cur.execute(formatted_query)
        # print(formatted_query)
        ret = cur.fetchall()
        new_ret = [(x[0], x[2],x[5]) for x in ret]
        return render_template('outputMovies.html', user=curr_user,name_of_user=session.get('username'), tuples=new_ret)
        
    elif link=='3':
        query = open('website/pysql/mp-celebs-alltime.txt', 'r').read()
        formatted_query = query.format()
        cur.execute(formatted_query)
        # print(formatted_query)
        ret = cur.fetchall()
        new_ret = [(x[0], x[1]) for x in ret]
        return render_template("outputPeople.html",user=curr_user,name_of_user=session.get('username') ,tuples=new_ret)

    elif link=='4':
        query = open('website/pysql/debuts-this-year.txt', 'r').read()
        formatted_query = query.format()
        cur.execute(formatted_query)
        # print(formatted_query)
        ret = cur.fetchall()
        new_ret = [(x[0], x[1], x[2], x[3]) for x in ret]
        return render_template("outputPeopleMovies.html",user=curr_user,name_of_user=session.get('username') ,tuples=new_ret)
    
    if link=='5':
        query = open('website/pysql/mp-shows.txt', 'r').read()
        formatted_query = query.format()
        cur.execute(formatted_query)
        # print(formatted_query)
        ret = cur.fetchall()
        new_ret = [(x[0], x[2], x[5], x[9]) for x in ret]
        return render_template('outputShowRatings.html', user=curr_user,name_of_user=session.get('username'), tuples=new_ret)
    
    if link=='6':
        query = open('website/pysql/mp-shows.txt', 'r').read()
        formatted_query = query.format()
        cur.execute(formatted_query)
        # print(formatted_query)
        ret = cur.fetchall()
        new_ret = [(x[0], x[2], x[5], x[9]) for x in ret]
        return render_template('outputShowRatings.html', user=curr_user,name_of_user=session.get('username'), tuples=new_ret)
    
    if link=='7':
        query = open('website/pysql/mp-shows.txt', 'r').read()
        formatted_query = query.format()
        cur.execute(formatted_query)
        # print(formatted_query)
        ret = cur.fetchall()
        new_ret = [(x[0], x[2], x[5], x[9]) for x in ret]
        return render_template('outputShowRatings.html', user=curr_user,name_of_user=session.get('username'), tuples=new_ret)

    # elif link==3:
    #     query = open('website/pysql/mp-movies-alltime.txt', 'r').read()
    #     formatted_query = query.format()
    #     cur.execute(formatted_query)
    #     # print(formatted_query)
    #     ret = cur.fetchall()
    # Here you can use the value of `link` to determine what output to show

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
        
@views.route('/person_info', methods=['GET', 'POST'])
def person_info():
    personid = request.args.get('personid')
    name = request.args.get('name')
    if not session.get('logged_in'):
        flash('You must login to continue to this page', category='error')
        return render_template("home.html",user=curr_user,name_of_user=session.get('username') )
    # if request.method == 'POST': 
        # person = request.form.get('p')#Gets the note from the HTML
    
    conn = create_db_connection()
    cur = conn.cursor()
 
    # query = "obama"  # the search query you want to make
    # url = f"https://www.google.com/search?q={query}&amp;tbm=isch"  # the URL of the search result page
    
    # print("the url searched is ",url)
    # response = requests.get(url)  # make a GET request to the URL
    # soup = BeautifulSoup(response.text, "html.parser")  # parse the HTML content with BeautifulSoup
    
    # # find the first image link by searching for the appropriate tag and attribute
    # img_tag = soup.find("img", {"class": "yWs4tf"})
    
    # if img_tag is not None:
    #     img_link = img_tag.get("src")
    #     print(img_link)  # print the first image link
    # else:
    #     print("No image found on the page.")


    query = open('website/pysql/person-info.txt', 'r').read()
    formatted_query = query.format(
        celebid='\''+personid+'\'',
    )
    cur.execute(formatted_query)
    # print(formatted_query)
    ret = cur.fetchall()
    return render_template("person_info.html",user=curr_user,name_of_user=session.get('username') , person_data=ret, person_name=name)

# @views.route('/recommendations', methods=['GET', 'POST'])
@views.route('/genreRecommend', methods=['GET', 'POST'])
def genreRec():
    user_email=session.get('curr_user')
    query = open('website/pysql/recommendations.txt', 'r').read()
    conn = create_db_connection()
    cur = conn.cursor()
    formatted_query = query.format(
        emailid='\''+user_email+'\'',
    )
    cur.execute(formatted_query)
    # print(formatted_query)
    ret = cur.fetchall()
    new_ret = [(x[0], x[1],x[2]) for x in ret]
    return render_template("outputMovies.html",user=curr_user,name_of_user=session.get('username') ,tuples=new_ret)

@views.route('/locRecommend', methods=['GET', 'POST'])
def locRec():
    user_email=session.get('curr_user')
    query = open('website/pysql/locRec.txt', 'r').read()
    conn = create_db_connection()
    cur = conn.cursor()
    formatted_query = query.format(
        emailid='\''+user_email+'\'',
    )
    cur.execute(formatted_query)
    # print(formatted_query)
    ret = cur.fetchall()
    new_ret = [(x[0], x[1],x[2]) for x in ret]
    return render_template("outputMovies.html",user=curr_user,name_of_user=session.get('username') ,tuples=new_ret)


@views.route('/celebRecommend', methods=['GET', 'POST'])
def celebRec():
    user_email=session.get('curr_user')
    query = open('website/pysql/celebRec.txt', 'r').read()
    conn = create_db_connection()
    cur = conn.cursor()
    formatted_query = query.format(
        emailid='\''+user_email+'\'',
    )
    cur.execute(formatted_query)
    # print(formatted_query)
    ret = cur.fetchall()
    new_ret = [(x[0], x[1],x[2]) for x in ret]
    return render_template("outputMovies.html",user=curr_user,name_of_user=session.get('username') ,tuples=new_ret)
    
    


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

