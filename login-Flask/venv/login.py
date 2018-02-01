from flask import Flask, render_template , url_for,request, session , redirect,jsonify
from flask_pymongo import PyMongo
import bcrypt
import jwt 
from bson import json_util,ObjectId
import config
import json
import datetime

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongoExample'
app.config['MONGO_URL'] = 'mongodb://localhost:27017/mongoExample'

mongo = PyMongo(app)

def checkArguments(check_list,req):
	for argument in check_list:
		if not argument in req:
			return False
	return True

def checkToken(token,userDb):

	secret_key = config.secretKey
	try:
		jwt_decode = jwt.decode(token,secret_key,algorithms=['HS256'])
		if jwt_decode['user_id'] == userDb['_id']:
			return True
		return False

	except jwt.InvalidTokenError:
		return False	

@app.route('/')
def index():
	if 'username' in session:
		return 'you are logged in as :', session['username']

	return render_template('index.html')

@app.route('/login',methods=['POST'])
def login():
	users = mongo.db.users
	req = request.get_json()
	secret_key = config.secretKey
	check_list = ['token','username','password']
	if checkArguments(check_list,req) :
		token = req['token']
		username = req['username']
		password = req['password']
		userDb = users.find_one({'username':username})
		if userDb:
			pwdHash = userDb['password']

			if checkToken(token,userDb):
				if bcrypt.hashpw(password.encode('UTF-8'),pwdHash.encode('UTF-8')) == pwdHash.encode('UTF-8'):
					response = {'status':True,'msg':'successfully login'}
					return jsonify(response)
				return 'wrong password'
			return 'Wrong Token'
		return 'No user'
	return 'Username/password/token not provided'

@app.route('/register',methods=['POST','GET'])
def register():
	
	users = mongo.db.users
	check_list = ['username','password']
	req = request.get_json()

	if checkArguments(check_list,req):
		username = req['username']
		password = req['password']
		existing_user = users.find_one({'username':username})

		if existing_user is None:
			hashpwd = bcrypt.hashpw(password.encode('UTF-8'),bcrypt.gensalt())
			user_id = repr(ObjectId())
			user = {'_id':user_id,'username':username,'password':hashpwd}
			user_json = json.loads(json_util.dumps(user))
			secret_key = config.secretKey
			payload = {'user_id':user_json['_id'],'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
                'iat': datetime.datetime.utcnow(),}
			token = jwt.encode(payload,secret_key,algorithm='HS256')
			user_json['token'] = token
			users.insert(user_json)
			response_json ={'id':user_json['_id'],'token':user_json['token']}
			return jsonify(response_json)

		return 'user exist'

	return ' provide suitable arguments'

if __name__ == '__main__':
	app.secret_key = 'mysecret'
	app.run(debug=True)

