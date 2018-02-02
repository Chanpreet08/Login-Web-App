from app import app
from app import models
from app import mongo
from flask import request,jsonify,abort
import bcrypt
import jwt 
from bson import json_util,ObjectId
import json
import datetime
from config import Config
from app import redis_store
from functools import wraps

token_expire = Config.TOKEN_EXPIRE

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):       
        req = request.get_json()
        token = req['token']
        username = req['username']
        users = mongo.db.users
        user_from_db = users.find_one({'username':username})
        user_from_db = json.loads(json_util.dumps(user_from_db))
        secret_key = user_from_db['accessKey']
        try:
            user = jwt.decode(token, secret_key, algorithms=['HS256'])
        except:
            abort(401)
        return f( *args, **kws)            
    return decorated_function


def generateToken(user):
	secret_key = user['accessKey']
	payload = {'user_id':user['_id']}
	token = jwt.encode(payload,secret_key,algorithm='HS256')
	return token

def validatePassword(password,db_hash):
	if bcrypt.checkpw(password.encode('utf-8'),db_hash.encode('utf-8')):
		return True
	return False

def generateAccessKey(user):
	username = user['username']
	user_id = user['_id']
	access_string = username + user_id
	access_key = bcrypt.hashpw(access_string.encode('utf-8'),bcrypt.gensalt())
	return access_key

def checkArguments(check_list,req):
	for argument in check_list:
		if not argument in req:
			return False 
	return True

def validateToken(token,user_from_db):
	secret_key = user_from_db['accessKey']
	try:
		jwt_decode = jwt.decode(token,secret_key,algorithms=['HS256'])
		if jwt_decode['user_id'] == user_from_db['_id']:
			if redis_store.get('token'):
				return True 
			return False
		return False

	except jwt.InvalidTokenError:
		return False	

def index():
	return redis_store.get('potato')


@app.route('/get_id',methods=['POST'])
@login_required
def getId():

	users =mongo.db.users
	req = request.get_json()
	check_list = ['username','token']
	if checkArguments(check_list,req):
		username = req['username']
		token = req['token']
		user_from_db = users.find_one({'username': username})
		user_from_db = json.loads(json_util.dumps(user_from_db))
		if user_from_db:
			user_id = user_from_db['_id']
			return jsonify(user_id)
		return 'No User'
    #return 'Provide Suitable Arguments'


@app.route('/login',methods=['POST'])
def login():

	users = mongo.db.users
	req = request.get_json()
	check_list = ['accessKey','username','password']
	if checkArguments(check_list,req) :
		access_key = req['accessKey']
		username = req['username']
		password = req['password']
		user_from_db = users.find_one({'username':username})
		if user_from_db:
			pwdHash = user_from_db['password']
			if access_key == user_from_db['accessKey']:
				if validatePassword(password,pwdHash):
					token = generateToken(user_from_db)
					redis_store.set(token,token)
					response = {'status':True,'msg':'successfully login','token':token}
					return jsonify(response)
				return 'wrong password'
			return 'Wrong accesskey'
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
		existing_user = users.find_one({'usrename':username})

		if existing_user is None:
			hashpwd = bcrypt.hashpw(password.encode('UTF-8'),bcrypt.gensalt())
			user_id = repr(ObjectId())
			user = {'_id':user_id,'username':username,'password':hashpwd}
			user_json = json.loads(json_util.dumps(user))
			access_key = generateAccessKey(user_json)
			user_json['accessKey'] = access_key
			users.insert(user_json)
			#redis_store.set(user_json['token'],user_json['token'],100)
			response_json ={'id':user_json['_id'],'accessKey':user_json['accessKey']}
			return jsonify(response_json)

		return 'user exist'

	return ' provide suitable arguments'

