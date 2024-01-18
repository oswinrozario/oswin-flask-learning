from flask import Blueprint

auth = Blueprint('auth', __name__,url_prefix='/api/v1/auth')

@auth.post('/register')
def register_controller():
  return 'user register '

@auth.post('/login')
def login_controller():
  return 'user login'