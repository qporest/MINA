from flask import Flask, request, session
from flask_pymongo import PyMongo
from user import User
# from flask.ext.login import login_user, logout_user, login_required
from flask_login import *
from MongoSession import *
import uuid

login_m = LoginManager()
app = Flask("Flow")
app.session_interface  = MongoSessionInterface(db="mongoSession")
login_m.init_app(app)
mongo = PyMongo()
mongo.init_app(app)

def load_user(user_id):
  users = mongo.db.users.find({"username": user_id})
  print users.count()
  if users.count() == 0:
    return None
  if users.count() == 1:
    return users[0]
  elif users.count() > 1:
    return users[0]
    print("There is "+str(users.count())+
      " users with id ["+str(user_id)+"]")

def load_post(post_id):
  posts = mongo.db.posts.find({"post_id": post_id})
  print posts.count()
  if posts.count() == 0:
    return None
  if posts.count() == 1:
    return posts[0]
  elif posts.count() > 1:
    return posts[0]
    print("There is "+str(posts.count())+
      " posts with id ["+str(post_id)+"]")

@login_m.user_loader
def load_user_obj(user_id):
  user = load_user(user_id)
  if not user:
    return None
  return User(user['_id'])

@app.route('/')
def index():
  return 'Index page here'

@app.route('/view')
def hello_word():
  return 'Viewing page here'

@app.route('/user/<username>')
def show_user_profile(username):
  # show the user profile for that user
  return 'User %s' % username

@app.route('/post/<int:post_id>', methods=["GET"])
def show_post(post_id):
  # show the post with the given id, the id is an integer
  post = load_post(post_id)
  if post:
    return "Post found"
  else:
    return "Such post doesn't exist"


@app.route('/post/keyword/<keyword>')
def find_post_by_keyword(keyword):
  pass

@app.route('/post', methods=["POST"])
@login_required
def post_post():
  content = request.get_json()
  post_id = uuid.uuid4()
  while load_post(post_id):
    post_id = uuid.uuid4()
  content["post_id"] = post_id
  mongo.db.posts.insert_one(content.data)
  #also add the reference to the list of user's posts
  return "Posted the post"

@app.route('/signup', methods=["POST"])
def signup():
  content = request.get_json()
  print "[Signup data] :"
  print content
  user = load_user(content['username'])
  print user
  if not user:
    User.create(content, mongo.db.users)
    return "User created"
  else:
    return "Error, this username is already used"

@app.route('/login', methods=["POST"])
def login():
  content = request.get_json()
  print "[Login data] :"
  print content
  user = load_user(content['username'])
  print user
  if user and User.validate_login(user['password'], content['password']):
    return "Logged in"
    session['username'] = user['username']
  else:
    return "Error, wrong username or password"

@app.route('/logout')
def logout():
  logout_user()
  return ""



