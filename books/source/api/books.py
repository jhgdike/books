from books.dals.models.book import BookAbstract, BookChapter
from books.ext import db
from books.source.schema.model_schema import books_schema, book_chapter_schema, book_chapters_schema


def get_book_list(category, limit, offset):
    book_list = BookAbstract.query.order_by(BookAbstract.id.desc()).limit(limit).offset(offset).all()
    return books_schema.dump(book_list).data


def get_book_chapter_detail(book_id, chapter_id):
    chapter = BookChapter.query.filter_by(book_id=book_id, chapter_id=chapter_id).first()
    return book_chapter_schema.dump(chapter).data


def get_book_chapter_list(book_id, limit=30, offset=0):
    chapter_list = db.session.query(BookChapter.chapter_id, BookChapter.title).filter(BookChapter.book_id == book_id).limit(
        limit).offset(offset).all()
    return book_chapters_schema.dump(chapter_list).data
