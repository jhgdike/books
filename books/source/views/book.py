from flask import Blueprint, request

from books.common.response import json_success
from books.source.api.books import get_book_list, get_book_chapter_detail, get_book_chapter_list

bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/list/')
def book_list():
    category = request.args.get('category', 0, type=int)
    limit = min(request.args.get('limit', 30, type=int), 30)
    offset = request.args.get('offset', 0, type=int)
    return json_success(get_book_list(category, limit, offset))


@bp.route('/<int:book_id>/chapter/')
def book_chapter_list(book_id):
    return json_success(get_book_chapter_list(book_id))


@bp.route('/<int:book_id>/chapter/<int:chapter_id>/')
def book_chapter(book_id, chapter_id):
    return json_success(get_book_chapter_detail(book_id, chapter_id))
