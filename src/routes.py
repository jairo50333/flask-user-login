from flask import render_template

from flask import render_template

from controllers.AddressController import AddressListApi
from controllers.PhonesController import PhoneListApi
from controllers.UserController import UserListApi
from src import app, api
from src.resources.authorization import AuthLogin


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


api.add_resource(UserListApi, '/users', '/users/<user_name>')
api.add_resource(PhoneListApi, '/users/phones', strict_slashes=False)
api.add_resource(AddressListApi, '/users/address', strict_slashes=False)
api.add_resource(AuthLogin, '/', strict_slashes=False)
