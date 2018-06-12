import requests, json, bcrypt, sys
from pprint import pprint
from db.base import DbManager
from db.entities import User, TVShow, Like

db = DbManager()
TVMAZE_SEARCH_URL = 'http://api.tvmaze.com/search/{}?q={}'
TVMAZE_GET_URL = 'http://api.tvmaze.com/{}/{}'

# SUPPORTING FUNCTIONS
def get_request(url):
   response = requests.get(url)
   return json.loads(response.text)


# DATA LAYER FUNCTIONS
# TVSHOW
def get_tvshow_by_api_id(api_id):
   db = DbManager()
   try:
      tvshow = db.open().query(TVShow).filter(TVShow.api_id == api_id).one()
      return tvshow
   except:
      tvshow = TVShow()
      url = TVMAZE_GET_URL.format('shows', api_id)
      response = get_request(url)
      tvshow.parse_json(response)
      db.save(tvshow)
      return tvshow

def search_tvshows(keyword):
   # always search from api first because it's all inclusive, search from db probably get less result
   db = DbManager()
   tvshows = []
   url = TVMAZE_SEARCH_URL.format('shows', keyword)
   for results in get_request(url):
      try:
         tvshow = db.open().query(TVShow).filter(TVShow.api_id == results['show']['id']).one()
      except:
         tvshow = TVShow()
         tvshow.parse_json(results['show'])
         db.save(tvshow)
      tvshows.append(tvshow)
   return tvshows


# USER
def create_user(name, email, password, confirm):
   error_message = []
   # 4 is not blank
   if len(name) == 0:
      error_message.append('Name cannot be empty')
   if len(email) == 0:
      error_message.append('Email cannot be empty')
   if len(password) == 0:
      error_message.append('Password cannot be empty')
   if len(confirm) == 0:
      error_message.append('Confirm Password cannot be empty')
   # password length more than 6
   if len(password) < 6:
      error_message.append('Password must be at least 6 character')
   # password and confirm is match
   if password != confirm:
      error_message.append('Password not match')

   if len(error_message) == 0:
      db = DbManager()
      try:
         user = User()
         user.name = name
         user.email = email
         encoded = password.encode('UTF-8')
         encrypted = bcrypt.hashpw(encoded, bcrypt.gensalt())
         user.password = password
         db.save(user)
         return user
      except:
         error_message.append('Email already exist')

   return error_message

def do_login(email, password):
   error_message = []
   db = DbManager()   
   # if user by email is exist
   try:
      user = db.open().query(User).filter(User.email == email).one()
      # check if password is match
      encoded_pass = password.encode('UTF-8')
      encrypted_pass = bcrypt.checkpw(encoded_pass, bcrypt.gensalt())
      if user.password == password:
         return user
      else:
         error_message.append('Incorect password')
   except:
      error_message.append("User doesn't exist")
   return error_message

def get_user_by_id(id):
   # GET USER BY ID
   db = DbManager()
   try:
      return db.open().query(User).filter(User.id == id).one()
   except:
      return None


# LIKE
def like_a_tvshow(user_id, api_id):
   # LIKE A TVSHOW
   # return a Like Model if success, if already exist return None
   tvshow = get_tvshow_by_api_id(api_id)
   db = DbManager()
   try:
      db.open().query(Like).filter(Like.user_id == user_id, Like.tvshow_id == tvshow.id).one()
      return None
   except:
      like = Like()
      like.user_id = user_id
      like.tvshow_id = tvshow.id
      db.save(like)
      return like

def unlike_a_tvshow(user_id, api_id):
   # UNLIKE TVSHOW
   tvshow = get_tvshow_by_api_id(api_id)
   db = DbManager()
   try:
      like = db.open().query(Like).filter(Like.user_id == user_id, Like.tvshow_id == tvshow.id).one()
      db.delete(like)
   except:
      return False

def get_user_likes(user_id):
   # GET USER LIKES
   # it gonna be return array-of-TVShow or empty-array
   db = DbManager()
   tvshows = []
   likes = db.open().query(Like).filter(Like.user_id == user_id).all()
   for like in likes:
      tvshows.append(like.tvshow)
   return tvshows

def get_user_likes_movie_id(user_id):
   db = DbManager()
   like_ids = []
   likes = db.open().query(Like).filter(Like.user_id == user_id).all()
   for like in likes:
      like_ids.append(like.tvshow.api_id)
   return like_ids