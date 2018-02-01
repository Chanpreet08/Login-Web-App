from flask import Flask,Blueprint
from flask_mongoalchemy import MongoAlchemy
from flask_pymongo import PyMongo
from flask_redis import FlaskRedis
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = MongoAlchemy(app)
mongo = PyMongo(app)
redis_store = FlaskRedis(app)
config = Config

def create_app():

	from views import *
	return app
 