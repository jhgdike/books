from datetime import datetime

from books.ext import db, ma


class BookAbstract(db.Model):
    __tablename__ = 'book_abstract'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, comment='书名')
    icon_url = db.Column(db.String(100), nullable=False, comment='图书icon')
    create_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    modify_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')


class BookChapter(db.Model):
    __tablename__ = 'book_chapter'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    book_id = db.Column(db.BigInteger, nullable=False, comment='书ID')
    chapter_id = db.Column(db.Integer, nullable=False, comment='章节')
    title = db.Column(db.String(20), nullable=False, comment='标题')
    body = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    modify_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    category = db.Column(db.String(20), nullable=False, comment='类别')


class BookSchema(ma.ModelSchema):
    class Meta:
        model = BookAbstract


class BookChapterSchema(ma.ModelSchema):
    class Meta:
        model = BookChapter


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category
