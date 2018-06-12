import sys

from db.entities import User
import db.data_layer as db

# RUN TEST

# SEARCH TVSHOW

def get_result(tvshow_from_search, tvshow_from_user_like):
   counter = 1
   user_likes = []
   for tvshow in tvshow_from_user_like:
      user_likes.append(tvshow.api_id)
   print(user_likes)

   for tvshow in tvshow_from_search:
      if tvshow.api_id in user_likes:
         print(tvshow.api_id, tvshow.name)

# get userlike
tvshow_from_search = db.search_tvshows('dody')
tvshow_from_user_like = db.get_user_likes(1)
get_result(tvshow_from_search, tvshow_from_user_like)

db.get_user_likes_movie_id

# # TEST CREATE USER
# result = db.create_user('Dody', 'dody2@gmail.com', '123123123', '123123123')
# if type(result) == User:
#    print(result.name)
# else:
#    for error in result:
#       print(error)

# # TEST LOGIN
# login = db.login('dody2@gmail.com', '23123123')
# if type(login ) == User:
#    print(login.name)
# else:
#    for error in login:
#       print(error)

# LIKE A TVSHOW
# db.like_a_tvshow(1,37081)

# UNLIKE A TVSHOW
# db.unlike_a_tvshow(1,123)

# GET USER LIKE
# tvshows = db.get_user_likes(1)
# for tvshow in tvshows:
#    print(tvshow.id, tvshow.name, tvshow.api_id)