from app import db

class User(db.Document):
	_id = db.ObjectIdField()
	username = db.StringField()
	password = db.StringField()
	accessString = db.StringField()
