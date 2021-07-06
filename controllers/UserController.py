from flask import request, render_template, make_response
from flask_restful import Resource
from marshmallow import ValidationError

from services.users_services import UserService, PhoneService, AddressService
from src import db
from src.resources.authorization import token_required
from src.schemas import UserSchema, PhoneSchema


class UserListApi(Resource):
    user_schema = UserSchema()
    phone_schema = PhoneSchema()

    @token_required
    def get(self, user_name=None):
        if not user_name:
            users = UserService.fetch_all_users(db.session).all()
            return make_response(render_template('users.html', users=users), 200)
        user = UserService.fetch_user_by_username(db.session, user_name)
        phones = PhoneService.fetch_phone_by_user_id(db.session, user.id).all()
        addresses = AddressService.fetch_address_by_user_id(db.session, user.id).all()
        if not user:
            return {'message', 'user not exists'}, 400
        return make_response(render_template('user.html', user=user, phones=phones, addresses=addresses), 200)

    def post(self):
        try:
            user = self.user_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.add(user)
        db.session.commit()
        return make_response(render_template('login.html'), 200)

    def put(self, user_name):
        user = UserService.fetch_user_by_username(db.session, user_name)
        if not user:
            return {'message', 'user not exists'}, 404
        try:
            user = self.user_schema.load(request.json, instance=user, session=db.session, partial=True)
        except ValidationError as e:
            return {'message', str(e)}, 404
        db.session.add(user)
        db.session.commit()
        return self.user_schema.dump(user), 200

    def patch(self):
        pass

    def delete(self, user_name):
        user = UserService.fetch_user_by_username(db.session, user_name)
        if not user:
            return "", 404
        db.session.delete(user)
        db.session.commit()
        """return "the user was deleted", 204"""
        return make_response(render_template('user.html', user=user), 200)
