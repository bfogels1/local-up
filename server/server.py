from flask import Flask, request, jsonify, send_from_directory
from models.shared import db # done
from controllers.import_controllers import import_controllers # done
from sqlalchemy.exc import IntegrityError
import os
import sys
from exceptions.basic_exception import BasicException

def create_test_app(self):
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['TESTING'] = True
    db.init_app(app)

    #with open('SPOTIFY_INFO', 'r') as f:
    #    lines = f.readlines()
    #    values = [line.strip().split('=')[1] for line in lines]
    #    app.config['SPOTIFY_USER'] = values[0]
    #    app.config['SPOTIFY_SECRET'] = values[1]

    return app

def create_real_app(testmode=False):
    app = create_app()
    #app.config['SPOTIFY_USER'] = os.environ.get('SPOTIFY_USER', None)
    #app.config['SPOTIFY_SECRET'] = os.environ.get('SPOTIFY_SECRET', None)
    if testmode:
        with open('DB_INFO', 'r') as f:
            lines = f.readlines()
            values = [line.strip().split('=')[1] for line in lines]
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(
                values[0], values[1], values[2], values[3])
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', None)
    db.init_app(app)
    return app

def create_app():

    #app = Flask(__name__, static_folder='../app/web/static', template_folder='../app/web/templates')
    app = Flask(__name__)
    import_controllers(app)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #@app.route('/')
    #def index():
    #    return send_from_directory(app.template_folder, "index.html")


    # @app.route('/choose_songs')
    # def choose_songs():
    #     return send_from_directory(app.template_folder, "choose_songs.html")

    # @app.route('/play_songs', endpoint='play_songs')
    # def play_songs():
    #     return send_from_directory(app.template_folder, "play_songs.html")
    
    # @app.route('/currently_playing')
    # def currently_playing():
    #     return send_from_directory(app.template_folder, "currently_playing.html")

    # @app.errorhandler(IntegrityError)
    # def sql_integrity_error(e):
    #     return jsonify({
    #         'message': str(e.orig)
    #     }), 400

    # @app.errorhandler(BasicException)
    # def unhandled_exception(e):
    #     print(e)
    #     return jsonify({
    #         'message': str(e)
    #     }), 400


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
    os.environ["PYTHONHASHSEED"] = "0"
    if '--testmode' in sys.argv:
        app = create_real_app(True)
        if '--port' in sys.argv:
            if (len(sys.argv) < 4):
                print('Usage: python3 server.py --testmode --port <port number>')
            else:
                app.run(debug = True, host=sys.argv[3], port=5000)
        else:
            app.run(debug = True)

    else:
        app = create_real_app()
        port = int(os.environ.get('PORT', 5000))
        app.run(debug=False, host="0.0.0.0", port=port)
