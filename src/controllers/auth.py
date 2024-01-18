from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth.post('/register')
def register_controller():
    try:
        return 'user register'
    except Exception as e:
        return f'Error during registration: {str(e)}', 500

@auth.post('/login')
def login_controller():
    try:
        return 'user login'
    except Exception as e:
        return f'Error during login: {str(e)}', 500
