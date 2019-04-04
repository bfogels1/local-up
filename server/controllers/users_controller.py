from flask import Blueprint, Flask, jsonify, request
#from tools.email_tools import email_is_valid
from tools.user_session_manager import log_in, log_out
from models.user import User
from models.user_passwords import UserPasswords
import random, string

app = Flask(__name__)
users_controller = Blueprint('users_controller', __name__)


class UsersController():

    @users_controller.route('/create', methods=['POST'])
    def create():
        json = request.get_json()
        username = json["username"]
        #display_name = json["display_name"]
        name = json["name"]
        email = json["email"]
        password = json["password"]
        #if not email_is_valid(email):
        #    return jsonify({
        #        'message': 'The e-mail provided is not in the correct format.'
        #    }), 400
        user = User(
            username=username,
            display_name=display_name,
            email=email,
        )
        token = user.insert(password)
        return jsonify({
            'data': {
                'user_id': user.id,
                'token': user.get_token()
            }
        }), 200

    @users_controller.route('/log_in', methods=['POST'])
    def log_in():
        json = request.get_json()
        username = json["username"]
        password = json["password"]
        user = User.query.filter(
            User.username == username
        ).first()
        token = log_in(user.id, password)
        print(token)
        if token is False:
            return jsonify({'message': 'Incorrect password.'}), 400 
        return jsonify({'token': token}), 200

    @users_controller.route('/log_out', methods=['POST'])
    def log_out():
        json = request.get_json()
        user_id = json["user_id"]
        token = json["token"]
        log_out(user_id, token)
        return jsonify({}), 200





