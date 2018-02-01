
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = 'mysecretkey'
	REDIS_URL = 'redis://localhost:6379/'
	MONGO_URL = 'mongodb://localhost:27017/'
	MONGOALCHEMY_DATABASE = 'mongoPractise'
	DEBUG = True
