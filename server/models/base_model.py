
from models.shared import db

class BaseModel():
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def save(self):
        db.session.commit()

    def serialize(self):
        to_return = {}
        chars_to_remove = len(self.__table__.name) + 1
        for column in self.__table__.columns:
            name = str(column)[chars_to_remove:]
            to_return[name] = self.__dict__[name]
        return to_return

