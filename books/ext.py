from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})
ma = Marshmallow()

ext_list = [db, cache, ma]
