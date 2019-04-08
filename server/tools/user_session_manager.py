from models.user_tokens import UserTokens # done
from models.user_passwords import UserPasswords # done
from tools.validation_tools import authenticate_user #done

def log_in(user_id, password):
    if UserPasswords.password_is_correct(user_id, password) is False:
        return False
    return UserTokens.create_new_token(user_id)

def log_out(user_id, token):
    authenticate_user(user_id, token)    
    user_token = UserTokens.query.filter(
        UserTokens.user_id == user_id,
        UserTokens.token == token
    ).first()
    user_token.deleted = True
    user_token.save()

