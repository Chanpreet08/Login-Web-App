from pyramid.config import Configurator

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from gridfs import GridFS
from pymongo import MongoClient
from pyramid.session import SignedCookieSessionFactory
my_session_factory = SignedCookieSessionFactory('pyramidtestapp')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """


    config = Configurator(settings=settings)
    db_url = urlparse(settings['mongo_uri'])
    config.registry.db = MongoClient(
       host=db_url.hostname,
       port=db_url.port,
    )

    def add_db(request):
        db = config.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
           db.authenticate(db_url.username, db_url.password)
        return db

    def add_fs(request):
        return GridFS(request.db)

    config.add_request_method(add_db, 'db', reify=True)
    config.add_request_method(add_fs, 'fs', reify=True)


    config.include('pyramid_jinja2')
    config.set_session_factory(my_session_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login','/login')
    config.add_route('signup','/signup')
    config.add_route('register','/register')
    config.scan()
    return config.make_wsgi_app()
