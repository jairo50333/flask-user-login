from src import db, models
'''
users = db.session.query(models.Users).join(models.Users.addresses).all()

phones = db.session.query(models.PhoneNumbers).filter_by(phone_number=564589791).first()
print(phones)
'''

