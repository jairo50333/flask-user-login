from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from services.users_services import AddressService
from src import db
from src.schemas import UserSchema, AddressSchema


class AddressListApi(Resource):
    address_schema = AddressSchema()
    user_schema = UserSchema()

    def post(self):
        try:
            address = self.address_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(address)
        db.session.commit()
        return self.address_schema.dump(address), 200

    def put(self):
        try:
            addressRequest = request.json
            address = AddressService.fetch_address_by_id(db.session, addressRequest["id"])
            if not address:
                return {'message', 'address not exists'}, 404
            address = self.address_schema.load(request.json, instance=address, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(address)
        db.session.commit()
        return self.address_schema.dump(address), 200

    def delete(self):
        addressRequest = request.json
        address = AddressService.fetch_address_by_id(db.session, addressRequest['id'])
        if not address:
            return "", 404
        db.session.delete(address)
        db.session.commit()
        return "the phone was deleted", 204
