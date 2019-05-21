from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .extention import *


from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta


class Model(object):
    """Baseclass for custom user models."""

    #: the query class used.  The :attr:`query` attribute is an instance
    #: of this class.  By default a :class:`BaseQuery` is used.
    # query_class = BaseQuery

    #: an instance of :attr:`query_class`.  Can be used to query the
    #: database for instances of this model.
    pass


def make_declarative_base():
    """Creates the declarative base."""
    base = declarative_base(cls=Model, name='Model', metaclass=_BoundDeclarativeMeta)
    return base


class _BoundDeclarativeMeta(DeclarativeMeta):
    def __init__(self, name, bases, d):
        bind_key = d.pop('__bind_key__', None)
        DeclarativeMeta.__init__(self, name, bases, d)
        if bind_key is not None:
            self.__table__.info['bind_key'] = bind_key


Base = make_declarative_base()
Base.to_dict = to_dict


AdLabReadSession = scoped_session(sessionmaker(class_=SignallingSession))
AdLabWriteSession = scoped_session(sessionmaker(class_=SignallingSession))


def _create_engine(user, password, host, port, db, pool_recycle=60, charset='utf8'):
    engine = create_engine('mysql://%s:%s@%s:%s/%s?charset=%s&use_unicode=1' % (
        user, password, host, port, db, charset),
                           pool_size=10,
                           max_overflow=-1,
                           pool_recycle=pool_recycle,
                           connect_args={'connect_timeout': 3, 'autocommit': 0},
                           )
    return engine
