import re
import db.data_layer as db
from flask import Flask, session, request, redirect, render_template, flash, url_for
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = '4102398471098rufhqoawpdh0q9234y57qpwuoi'
csrf = CSRFProtect(app)

# SUPPORTING FUNCTION
def setup_web_session(user):
    session['user_id'] = user.id
    session['user_name'] = user.email
    session['name'] = user.name

# HOMEPAGE
@app.route('/')
def index():
    # SHOW USER LIKES 
    if 'user_id' in session:
        tvshows = db.get_user_likes(session['user_id'])
        user_likes = db.get_user_likes_movie_id(session['user_id'])
    else:
        tvshows = []
        user_likes = []
    return render_template('index.html', tvshows = tvshows, user_likes = user_likes)

# USER
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        login_result = db.do_login(email, password)
        if(type(login_result) == list):
            for error in login_result:
                flash(error)
            return redirect(url_for('login'))
        else:
            setup_web_session(login_result)
            return redirect(url_for('index'))
    else:
        return render_template('user/login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# TVSHOW
@app.route('/tvshow/search/<keyword>', methods=['GET'])
def getsearch(keyword):
    if 'user_id' in session:
        user_likes = db.get_user_likes_movie_id(session['user_id'])
    else:
        user_likes = []
    tvshows = db.search_tvshows(keyword)
    return render_template('index.html', tvshows = tvshows, user_likes = user_likes)

@app.route('/tvshow/search', methods=['POST'])
def postsearch():
    keyword = request.form['tvshow_search_keyword']
    return redirect(url_for('getsearch', keyword = keyword))

@app.route('/tvshow/like/<user_id>/<api_id>')
def like_tvshow(user_id, api_id):
    db.like_a_tvshow(user_id, api_id)
    return redirect(request.referrer)

@app.route('/tvshow/unlike/<user_id>/<api_id>')
def unlike_tvshow(user_id, api_id):
    db.unlike_a_tvshow(user_id, api_id)
    return redirect(request.referrer)



app.jinja_env.auto_reload = True
app.config['TEMPLATE_AUTO_RELOAD'] = True
app.run(debug=True, use_reloader = True)