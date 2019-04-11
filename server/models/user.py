import random, string
from models.shared import db # done
from models.base_model import BaseModel # done
from models.user_tokens import UserTokens # done
from models.user_passwords import UserPasswords # done


class User(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    #display_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def insert(self):
        raise NotImplementedError()

    def insert(self, password):
        # TODO make this a transaction so that user and password both get inserted (or not)
        super(User, self).insert()
        UserPasswords.create_password(self.id, password)
        UserTokens.create_new_token(self.id)

    def get_token(self):
        user_token = UserTokens.query.filter(
            UserTokens.user_id == self.id,
            UserTokens.deleted == False
        ).one()
        return user_token.token

