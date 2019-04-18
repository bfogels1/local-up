from flask import Flask, request, jsonify, abort
#import json
#from models.shared import db  # done
#from firebase import Firebase
import json
import firebase_admin
from firebase_admin import db, credentials
#from controllers.import_controllers import import_controllers  # done
#from sqlalchemy.exc import IntegrityError
from tools.password_encryption import encode_password
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

    USERS = db.reference('users')

    @app.route('/users/create', methods=['POST'])
    def create_user():
        req = request.json

        name = req["name"]
        email = req["email"]
        encoded_password = encode_password(req["password"])
        
        user = USERS.push({
            'name': name,
            'email': email,
            'password': encoded_password
          });

        return jsonify({'id': user.key}), 201


    @app.route('/users/login', methods=['POST'])
    def login_user():
        json = request.json
        email = json["email"]
        password = json["password"]
        encoded_password = encode_password(password)

        snapshot = USERS.order_by_child('email').equal_to(email).get()
        for key, val in snapshot.items():
            retrieved_password = val['password']

        print(retrieved_password)
        print(encoded_password)
        if not snapshot:
            return jsonify({'message': 'Invalid Email'}), 400
        if retrieved_password != encoded_password:
            return jsonify({'message': 'Incorrect Password'}), 400
        return jsonify({'message': 'Success'}), 201

        # if _ensure_user(email):
        #     user = USERS.child(email).get()
        #     actual_password = user[password]
        #     if encoded_password == actual_password:
        #         return jsonify({'message': 'Success'}), 201
        #     return jsonify({'message': 'Incorrect Password'}), 400
        # return jsonify({'message': 'Invalid Email'}), 400

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
 