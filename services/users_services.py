from src.models import Users, PhoneNumbers, Addresses


class UserService:
    @staticmethod
    def fetch_all_users(session):
        return session.query(Users)

    @classmethod
    def fetch_user_by_username(cls, session, user_name):
        return cls.fetch_all_users(session).filter_by(user_name=user_name).first()

    @classmethod
    def fetch_user_by_email(cls, session, email):
        return cls.fetch_all_users(session).filter_by(email=email).first()

    @classmethod
    def fetch_users_by_name(cls, session, name):
        return cls.fetch_all_users(session).filter(Users.first_name.contains(name) | Users.last_name.contains(name))


class PhoneService:
    @staticmethod
    def fetch_all_phones(session):
        return session.query(PhoneNumbers)

    @classmethod
    def fetch_phone_by_user_id(cls, session, id):
        return cls.fetch_all_phones(session).filter_by(user_id=id)

    @classmethod
    def fetch_phone_by_id(cls, session, id):
        return cls.fetch_all_phones(session).filter_by(id=id).first()


class AddressService:
    @staticmethod
    def fetch_all_address(session):
        return session.query(Addresses)

    @classmethod
    def fetch_address_by_user_id(cls, session, id):
        return cls.fetch_all_address(session).filter_by(user_id=id)

    @classmethod
    def fetch_address_by_id(cls, session, id):
        return cls.fetch_all_address(session).filter_by(id=id).first()
