from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from services.users_services import PhoneService
from src import db
from src.schemas import UserSchema, PhoneSchema


class PhoneListApi(Resource):
    phone_schema = PhoneSchema()
    user_schema = UserSchema()

    def post(self):
        try:
            phone = self.phone_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(phone)
        db.session.commit()
        return self.phone_schema.dump(phone), 200

    def put(self):
        try:
            phoneRequest = request.json
            phone = PhoneService.fetch_phone_by_id(db.session, phoneRequest['id'])
            phone = self.phone_schema.load(request.json, instance=phone, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(phone)
        db.session.commit()
        return self.phone_schema.dump(phone), 200

    def delete(self):
        phoneRequest = request.json
        phone = PhoneService.fetch_phone_by_id(db.session, phoneRequest['id'])
        if not phone:
            return "", 404
        db.session.delete(phone)
        db.session.commit()
        return "the phone was deleted", 204
