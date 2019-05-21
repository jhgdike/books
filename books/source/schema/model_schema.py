from books.dals.models.book import BookSchema, BookChapterSchema, CategorySchema


book_schema = BookSchema()
books_schema = BookSchema(many=True)
book_chapter_schema = BookChapterSchema()
book_chapters_schema = BookChapterSchema(many=True)
category_schema = CategorySchema()
categorys_schema = CategorySchema(many=True)
