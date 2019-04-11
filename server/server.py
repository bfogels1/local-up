from flask import Flask, request, jsonify, abort
#from models.shared import db  # done
import firebase_admin
from firebase_admin import db
#from controllers.import_controllers import import_controllers  # done
#from sqlalchemy.exc import IntegrityError
import os
import sys
from exceptions.basic_exception import BasicException

def create_app():
    app = Flask(__name__)

    firebase_admin.initialize_app(options={
        'databaseURL': 'https://localup-34dd4.firebaseio.com'
    })
    USERS = db.reference('users')

    @app.route('/users/create', methods=['POST'])
    def create_user():
        req = request.json
        user = USERS.push(req)
        return jsonify({'id': user.key}), 201

    # @app.route('/heroes/<id>')
    # def read_hero(id):
    #     return flask.jsonify(_ensure_hero(id))

    # @app.route('/heroes/<id>', methods=['PUT'])
    # def update_hero(id):
    #     _ensure_hero(id)
    #     req = flask.request.json
    #     SUPERHEROES.child(id).update(req)
    #     return flask.jsonify({'success': True})

    # @app.route('/heroes/<id>', methods=['DELETE'])
    # def delete_hero(id):
    #     _ensure_hero(id)
    #     SUPERHEROES.child(id).delete()
    #     return flask.jsonify({'success': True})

    # def _ensure_user(id):
    #     user = USERS.child(id).get()
    #     if not user:
    #         abort(404)
    #     return user

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
 