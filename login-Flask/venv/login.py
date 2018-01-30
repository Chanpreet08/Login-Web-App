from flask import Flask, render_template , url_for,request, session , redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongoExample'
app.config['MONGO_URL'] = 'mongodb://localhost:27020/mydb'

mongo = PyMongo(app)

@app.route('/')
def index():
	if 'username' in session:
		return 'you are logged in as :', session['username']

	return render_template('index.html')

@app.route('/login',methods=['POST'])
def login():
	users = mongo.db.users
	login_user = users.find_one({"name":request.form['username']})

	if login_user:
		if bcrypt.hashpw(request.form['pass'].encode('UTF-8'),login_user['password'].encode('UTF-8')) == login_user['password'].encode('UTF-8'):
			session['username'] = request.form['username']
			return redirect(url_for('index'))

		return 'Invalid username/password'

	return 'No User found'


@app.route('/register',methods=['POST','GET'])
def register():
	if request.method == 'POST':
		users = mongo.db.users
		existing_user = users.find_one({'name':request.form['username']})

		if existing_user is None:
			hashpwd = bcrypt.hashpw(request.form['pass'].encode('UTF-8'),bcrypt.gensalt())
			users.insert({'name':request.form['username'],'password':hashpwd})
			session['username'] = request.form['username']
			return url_for('index')

		return 'username already exist'

	return render_template('register.html')

if __name__ == '__main__':
	app.secret_key = 'mysecret'
	app.run(debug=True)

