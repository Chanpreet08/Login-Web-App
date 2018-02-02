
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = 'mysecretkey'
	REDIS_URL = 'redis://localhost:6379/0'
	MONGO_URL = 'mongodb://localhost:27017/'
	MONGO_DBNAME = 'mongoExample'
	MONGOALCHEMY_DATABASE = 'mongoExample'
	TOKEN_EXPIRE = 1000

