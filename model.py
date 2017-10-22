from main import load_user, load_post
class UserModel():

  def __init__(self, username):
    user = load_user(username)
    if not user:
      return
    self.username = user['username']
    #because the username shouldn't be really changed
    self._username = user['username']
    self.password = user['password']
    self.posts = user['posts']

  def get_current_obj(self):
    return {
      "username": self._username,
      "password": self.password,
      "posts": self.posts
    }

class PostModel():
  def __init__(self, post_id):
    post = load_post(post_id)
    if not post:
      return
    self.post_id = post['post_id']
    #because we don't want the post id to change
    self._post_id = post['post_id']
    self.description = post['description']
    self.links = post['links']
    self.likes = post['likes']
    self.keyword = post['keywords']

  def get_current_obj(self):
    return {
      "post_id": self._post_id,
      "description": self.description,
      "links": self.links,
      "likes": self.likes,
      "keywords": self.keywords
    }
