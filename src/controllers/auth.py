from flask import Blueprint, request, jsonify
from flask_restful import Resource, reqparse
from passlib.hash import bcrypt
from src.service.db import db
from src.models.user import User
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth.post('/register')
def register_controller():
    
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')

        try:
            data = parser.parse_args(strict=True)
        except:
            return {'message': 'Invalid or missing JSON data'}, 400

        if not data['username'] or not data['email'] or not data['password']:
            return {'message': 'Username, email, and password are required'}, 400

        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username already taken'}, 400

        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already taken'}, 400

        hashed_password = bcrypt.hash(data['password'])

        new_user = User(username=data['username'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        user_dict = {'id': new_user.id, 'username': new_user.username, 'email': new_user.email}

        return {'message': 'User registered successfully', 'user': user_dict}, 201
    except Exception as e:
        return {'error': 'Error during registration'}, 500

    

@auth.post('/login')
def login_controller():
    
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')

        try:
            data = parser.parse_args(strict=True)
        except:
            return {'message': 'Invalid or missing JSON data'}, 400
        
        email = request.json.get('email', '')
        password = request.json.get('password', '')
        
        if not email or not password:
            return {'message': 'Email, and password are required'}, 400

        user = User.query.filter_by(email=email).first()

        if user:
            is_pass_correct = bcrypt.verify(password,user.password)

            if is_pass_correct:
                refresh = create_refresh_token(identity=user.id)
                access = create_access_token(identity=user.id)

                return jsonify({
                    'user': {
                        'refresh_token': refresh,
                        'access_token': access,
                        'username': user.username,
                        'email': user.email,
                        'id':user.id,
                    }

                }), 200
            return jsonify({'error': 'Wrong password'}), 401

        return jsonify({'error': 'User Not Found'}), 401
    except Exception as e:
        return {'error': 'Error during login'}, 500
