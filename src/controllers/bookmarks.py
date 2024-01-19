from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from src.models.bookmark import Bookmark
from src.models.user import User
from src.service.db import db
import validators

bookmarks = Blueprint('bookmarks', __name__,url_prefix='/api/v1/bookmarks')

@bookmarks.route('', methods=['POST', 'GET'])
@jwt_required()
def list_create_bookmarks_controller():
    current_user = get_jwt_identity()
    if request.method == 'GET':
        try:
            
            if User.query.filter_by(id=current_user).first() is None:
                raise Exception
            
            bookmarks_fetched = Bookmark.query.filter_by(
            user_id=current_user)

            data = []
            print(data)
            print(bookmarks_fetched)
            for bookmark in bookmarks_fetched:
                print(bookmark)
                data.append({
                    'id': bookmark.id,
                    'url': bookmark.url,
                    'short_url': bookmark.short_url,
                    'visit': bookmark.visits,
                    'body': bookmark.body,
                    'created_at': bookmark.created_at,
                    'updated_at': bookmark.updated_at,
                })
                print(bookmark)
            print(data)
            return jsonify({'data': data}), 200
        except Exception as e:
            return {'error':'Something went wrong'}, 500
    else:
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('url', type=str, required=True, help='Url is required')
            parser.add_argument('body', type=str, required=True, help='Body is required')

            try:
                data = parser.parse_args(strict=True)
            except:
                return {'message': 'Invalid or missing JSON data'}, 400
            
            url = request.json.get('url','')
            body = request.json.get('body','')

            if not validators.url(url):
                return jsonify({
                    'error': 'Enter a valid url'
                }), 400
                
            if Bookmark.query.filter_by(url=url,user_id=current_user).first():
                return jsonify({
                    'error': 'URL already exists'
                }), 409
            
            if User.query.filter_by(id=current_user).first() is None:
                raise Exception
                
            
            bookmark = Bookmark(url=url, body=body, user_id=current_user)
            
            db.session.add(bookmark)
            db.session.commit()
            
            return jsonify({
                'id': bookmark.id,
                'url': bookmark.url,
                'short_url': bookmark.short_url,
                'visit': bookmark.visits,
                'body': bookmark.body,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at,
            }), 201
        
        except Exception as e:
            return {'error':'Something went wrong'}, 500
        
@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmark(id):
    try:
        current_user = get_jwt_identity()
        if User.query.filter_by(id=current_user).first() is None:
            return jsonify({'error': 'User not found'}), 404
        bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()
        if not bookmark:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visit': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at,
        }), 200
    except Exception as e:
        return {'error':'Something went wrong'}, 500    
        
        
@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark_controller(id):
    try:
        current_user = get_jwt_identity()
        bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()
        if not bookmark:
            return jsonify({'message': 'Item not found'}), 404
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify({'error': 'Item deleted successfully'}), 200
    except Exception as e:
        return {'error':'Something went wrong'}, 500


@bookmarks.put('/<int:id>')
@bookmarks.patch('/<int:id>')
@jwt_required()
def editbookmark(id):
    try:
        current_user = get_jwt_identity()
        bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()
        if not bookmark:
            return jsonify({'message': 'Item not found'}), 404
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')
        if body is '' and url is '':
            return {'error':'Nothing to update'}, 400
        if url and not validators.url(url):
            return jsonify({
                'error': 'Enter a valid url'
            }), 400
        if Bookmark.query.filter_by(url=url, user_id=current_user).first():
            return jsonify({
                'error': 'URL already exists'
            }), 409
        if body is not '':
            bookmark.body = body
        if url is not '':
            bookmark.url = url
        db.session.commit()
        return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visit': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at,
        }), 200
    except Exception as e:
        return {'error':'Something went wrong'}, 500