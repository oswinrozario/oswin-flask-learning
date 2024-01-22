from flask import Flask, Blueprint, jsonify, redirect
from src.models.bookmark import Bookmark
from src.service.db  import db

short_url_blueprint = Blueprint('short_url', __name__, url_prefix='')

@short_url_blueprint.route('/<short_url>')
def short_url_controller(short_url):
  try:
    short_url = Bookmark.query.filter_by(short_url=short_url).first()
    if not short_url:
      return jsonify({'error': 'Url not found'}), 404
    short_url.visits += 1
    db.session.add(short_url)
    db.session.commit()
    return redirect(short_url.url)
  except Exception as e:
    return jsonify({'error': 'Something went wrong'}), 500