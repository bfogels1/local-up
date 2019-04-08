import random, string
import hashlib
from models.shared import db # done
from models.base_model import BaseModel # done
from tools.user_session_tools import password_is_valid # done
from exceptions.invalid_password_exception import InvalidPasswordException # done


class UserPasswords(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    salt = db.Column(db.String, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def create_password(user_id, password):
        if password_is_valid(password) is False:
            raise InvalidPasswordException()
        current_password = UserPasswords.query.filter(
            UserPasswords.user_id == user_id,
            UserPasswords.deleted == False
        ).first()
        if current_password is not None:
            current_password.deleted = True
            current_password.save()
        salt = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(50))
        password_hash = hash(password + salt)
        UserPasswords(user_id=user_id, salt=salt, hashed_password=password_hash).insert()

    @staticmethod
    def password_is_correct(user_id, password):
        user_password = UserPasswords.query.filter(
            UserPasswords.user_id == user_id,
            UserPasswords.deleted == False
        ).first()
        #m = hashlib.md5()
        #m.update(password + user_password.salt)
        #print(m.digest())
        print("TODO: CHANGE HASH FUNCTION")
        password_hash = hash(password + user_password.salt)
        return password_hash == int(user_password.hashed_password)



