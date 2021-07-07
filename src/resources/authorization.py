import datetime
from functools import wraps

import jwt
from flask import request, jsonify, render_template, make_response, redirect, url_for
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from services.users_services import UserService
from src import db, app
from src.models import Users
from src.schemas import UserSchema


class AuthRegister(Resource):
    user_schema = UserSchema()

    def post(self):
        try:
            user = self.user_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}
        try:
            db.session().add(user)
            db.session.commit()
        except IntegrityError:
            db.session.roleback()
            return {'message', 'such user exists'}, 409
        return self.user_schema.dump(user), 201


class AuthLogin(Resource):
    user_schema = UserSchema()

    def post(self):
        login = request.form.get('email')
        password = request.form.get('password')
        user = UserService.fetch_user_by_email(db.session, login)
        if not user or not check_password_hash(user.password, password):
            return "user not found", 401, {"WWW-Authenticate": "basic_realm :'Authentication required'"}
        '''
        token = jwt.encode(
            {
                "user_id": user.user_name,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY']
        )
        jsonify(
            {
                "token": token.decode('utf-8')
            }
        )'''
        return redirect(url_for('userlistapi'))


def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.headers.get('X-api-key', '')
        if not token:
            return "", 401, {"WWW-Authenticate": "basic_realm :'Authentication required'"}
        try:
            user_name = jwt.decode(token, app.config['SECRET_KEY'])['user_id']
        except(KeyError, jwt.ExpiredSignatureError):
            return "", 401, {"WWW-Authenticate": "basic_realm :'Authentication required'"}
        user = db.session.query(Users).filter_by(user_name=user_name).first()
        # user = Users.find_user_by_uuid(uuid)
        if not user:
            return "", 401, {"WWW-Authenticate": "basic_realm :'Authentication required'"}
        return func(self, *args, **kwargs)

    return wrapper
