from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from src.models import Users, Addresses, PhoneNumbers


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        load_only = ('password')

    addresses = Nested('AddressSchema', many=True)
    phone_numbers = Nested('PhoneSchema', many=True)


class AddressSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Addresses
        load_instance = True
        include_fk = True


class PhoneSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PhoneNumbers
        load_instance = True
        include_fk = True
