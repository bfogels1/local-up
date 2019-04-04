import random, string
from models.shared import db #done
from models.base_model import BaseModel #done


class UserTokens(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String, nullable=False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    #def create_new_token(self, user_id):
    def create_new_token(user_id):
        UserTokens._deactivate_current_token(user_id)
        user_token = True
        while user_token != None:
            token = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(45))
            user_token = UserTokens.query.filter(UserTokens.token == token, UserTokens.user_id == user_id).first()
        UserTokens(user_id=user_id, token=token).insert()
        return token

    @staticmethod
    def _deactivate_current_token(user_id):
        user_token = UserTokens.query.filter(
            UserTokens.user_id == user_id,
            UserTokens.deleted == False
        ).first()
        if user_token is not None:
            user_token.deleted = True
            user_token.save()


