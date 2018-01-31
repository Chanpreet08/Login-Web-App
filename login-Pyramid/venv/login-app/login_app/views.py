from pyramid.view import view_config
from pymongo import MongoClient
import bcrypt
from pyramid.response import Response

@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'cc'}

@view_config(route_name='login', renderer='json')
def login(request):

    if 'form.submitted' in request.params:
        username = request.params['username']
        password = request.params['password']
        loggedUser = request.db['users'].find_one({'username':username})

        if loggedUser:
	        hashpwd = loggedUser['password'].encode('utf-8')
	        if bcrypt.checkpw(password.encode('utf-8'),hashpwd):
	        	request.session['username']= username
	        	return {'success':True,'msg':'successful login'}
	        else:
	        	return {'success':False,'msg':'Wrong password'}  

	return {'sucess':False,'msg':'No User'}    

@view_config(route_name='signup', renderer ='templates/registertemplate.jinja2')
def signup(request):
	return ''

@view_config(route_name='register', renderer ='json')
def register(request):
	if 'form.submitted' in request.params:
		username = request.params['username']
		password = request.params['password']
		user = request.db['users'].find_one({'username':username})
		if not user:
			hashpwd = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
			request.db['users'].insert({'username':username,'password':hashpwd})
			request.session['username'] = username
			return {'success':True,'msg':'User created'}
		else:
			return {'sucess':False,'msg':'Username exist'}

    