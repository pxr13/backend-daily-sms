from sqlalchemy import Column, Integer, String, Boolean
from src.extensions import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    phone_number = Column(Integer, unique=True, nullable=False)
    verified = Column(Boolean, nullable=False, default=True)
    code = Column(Integer, unique=True)

    def __init__(self, **kwargs):
        # preserve SQLAlchemy's built in constructor functionality
        super(UserModel, self).__init__(**kwargs)
        self.phone_number = kwargs['phone_number']

    @classmethod
    def find_by_phone_number(cls, phone_number):
        return cls.query.filter_by(phone_number=phone_number).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
