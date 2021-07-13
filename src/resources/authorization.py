import datetime
from functools import wraps
import jwt
from flask import request, session, redirect, url_for
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
        addressRequest = request.json
        user = UserService.fetch_user_by_email(db.session, addressRequest["email"])
        if not user or not check_password_hash(user.password, addressRequest["password"]):
            return "user not found", 401
        session.permanent = True
        session['users'] = addressRequest["email"]
        """return redirect(url_for("userlistapi")), 200"""
        return "ok"

    def delete(self):
        session.pop("users", None)
        return "OK"


def getSession(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not "users" in session:
            return "need authorization to enter in the current page", 401, {"WWW-Authenticate": "basic_realm :'Authentication required'"}
        return func(self, *args, **kwargs)
    return wrapper
