from flask import Blueprint

bookmarks = Blueprint('bookmarks', __name__,url_prefix='/api/v1/bookmarks')

@bookmarks.get('/')
def list_bookmarks_controller():
    try:
        return 'user bookmarks'
    except Exception as e:
        return f'Error fetching bookmarks: {str(e)}', 500