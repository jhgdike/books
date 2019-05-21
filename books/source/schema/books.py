from marshmallow import fields, Schema


class BookSchema(Schema):
    """"""
    id = fields.Integer()
    name = fields.String()
    icon_url = fields.URL()
    create_at = fields.DateTime()
    modify_at = fields.DateTime()


book_list_schema = BookSchema(many=True)
