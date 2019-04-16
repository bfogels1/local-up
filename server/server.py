from flask import Flask, request, jsonify, abort
#import json
#from models.shared import db  # done
#from firebase import Firebase
import json
import firebase_admin
from firebase_admin import db, credentials
#from controllers.import_controllers import import_controllers  # done
#from sqlalchemy.exc import IntegrityError
from tools.password_encryption import encode_password, decode_password
#from models.user import User
import os
import sys
from exceptions.basic_exception import BasicException

def create_app():
    app = Flask(__name__)

    cred = credentials.Certificate("localup-42a2d0b55f0b.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL' : 'https://localup-34dd4.firebaseio.com'
    })

    #firebase = firebase.FirebaseApplication(‘https://localup-34dd4.firebaseio.com’, None)


    USERS = db.reference('users')

    @app.route('/users/create', methods=['POST'])
    def create_user():
        req = request.json
        name = req["name"]
        email = req["email"]
        encoded_password = encode_password(req["password"])
        # data = {
        #    'email' : email,
        #    'name' : name,
        #    'password' : encoded_password
        #}

        user = USERS.push({
           'email' : email,
           'name' : name,
           'password' : encoded_password
        })

        #encoded_data = json.JSONEncode(data)

        #user = USERS.push(encoded_data)
        
        #user = USERS.push(req)

        return jsonify({'id': user.key}), 201

    # @app.route('/users/create', methods=['POST'])
    # def create_user():
    #     req = request.json
    #     name = req["name"]
    #     email = req["email"]
    #     password = req["password"]
    #     encoded_password = encode_password(password)
    #     #print('here 1')
    #     #user = User(
    #     #    #name=name,
    #     #    #email=email,
    #     #    #password = encode_password(password),
    #     #    #password =password,
    #     #)
    #     #data = jsonify(name=name,password=encoded_password)
    #     data = {
    #         'name' : name,
    #         'password' : encoded_password
    #     }
    #     #print('here 2')

    #     #json = jsonify(data)

    #     #USERS.child(email).set(json.dumps(data))
    #     #USERS.child(email).put(data)
    #     #USERS.child(email).push(json)
    #     USERS.push(data)
    #     #USERS.push(json)
    #     #print('here 3')
    #     #USERS.push(json)
    #     return jsonify({'message': 'Success'}), 201

    # @app.route('/users/login', methods=['POST'])
    # def login_user():
    #     json = request.json
    #     email = json["email"]
    #     password = json["password"]
    #     encoded_password = encode_password(password)
    #     if _ensure_user(email):
    #         user = USERS.child(email).get()
    #         actual_password = user[password]
    #         if encoded_password == actual_password:
    #             return jsonify({'message': 'Success'}), 201
    #         return jsonify({'message': 'Incorrect Password'}), 400
    #     return jsonify({'message': 'Invalid Email'}), 400

    # def _ensure_user(email):
    #      user = USERS.child(email).get()
    #      if not user:
    #          return False
    #      return True

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        print(e)
        return jsonify({
            'message': 'An unexpected error occurred.'
        }), 400

    @app.route('/<path:path>')
    def catch_all(path):
        return 'ROUTE NOT FOUND'
    return app

if __name__ == "__main__":
    if '--testmode' in sys.argv:
        app = create_app()
        if '--port' in sys.argv:
            if len(sys.argv) < 4:
                print('Usage: python3 server.py --testmode --port <port number>')
            else:
                app.run(debug=True, host=sys.argv[3], port=5000)
        else:
            app.run(debug=True)
    else:
        app = create_app()
        port = int(os.environ.get('PORT', 5000))
        app.run(debug=False, host="0.0.0.0", port=port)
 