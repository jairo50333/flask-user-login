from datetime import date

from src import db
from src.models import Users, Addresses, PhoneNumbers


def populate_users():
    jairo = Users(
        first_name="jair",
        last_name="rincon",
        password="admin",
        email="juanp@gmail.com",
        date_of_birth=date(2001, 12, 18),
    )
    address = Addresses(
        user_id=2,
        street="zorge",
        zip=1254,
        city="rostov",
        country="russia"
    )
    phone = PhoneNumbers(
        phone_number="+415479831",
        user_id=2
    )

    '''
    jairo.addresses = address

    db.session.add(jairo)
    db.session.add(address)
    '''
    db.session.add(phone)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    print("adding users")
    populate_users()
    print("users added")
