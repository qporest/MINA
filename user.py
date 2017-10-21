from werkzeug.security import check_password_hash, generate_password_hash

class User():

  def __init__(self, username):
    self.username = username

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return self.username

  @staticmethod
  def create(obj, db):
    db.insert_one({"username": obj['username'],
      "password": generate_password_hash(obj['password'])})

  @staticmethod
  def validate_login(password_hash, password):
    return check_password_hash(password_hash, password)
