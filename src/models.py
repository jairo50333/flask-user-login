from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash

from src import db
import uuid


class Users(db.Model):
    __tableName__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    user_name = db.Column(db.String(8), unique=True)
    password = db.Column(db.String(254), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, index=True, nullable=False)
    phone_numbers = db.relationship("PhoneNumbers")
    addresses = db.relationship("Addresses")

    def __init__(self, first_name, last_name, password, email, date_of_birth, phone_numbers=None, addresses=None):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = str(uuid.uuid4())[:8]
        self.password = generate_password_hash(password)
        self.email = email
        self.date_of_birth = date_of_birth
        if not phone_numbers:
            self.phone_numbers = []
        else:
            self.phone_numbers = phone_numbers
        if not addresses:
            self.addresses = []
        else:
            self.addresses = addresses

    def __repr__(self):
        return f'User({self.first_name, self.last_name, self.email, self.addresses})'


class PhoneNumbers(db.Model):
    __tableName__ = 'phoneNumbers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    phone_number = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, phone_number):
        self.user_id = user_id
        self.phone_number = phone_number

    def __repr__(self):
        return f'Phone:({self.phone_number})'


class Addresses(db.Model):
    __tableName__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    street = db.Column(db.String(20), nullable=False)
    zip = db.Column(db.Integer, nullable=True)
    city = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)

    def __init__(self, user_id, street, zip, city, country):
        self.user_id = user_id
        self.street = street
        self.zip = zip
        self.city = city
        self.country = country

    def __repr__(self):
        return f'address({self.zip, self.country, self.city, self.street})'
