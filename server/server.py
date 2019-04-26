from flask import Flask, request, jsonify, abort
# import json
# from models.shared import db  # done
# from firebase import Firebase
import json
import firebase_admin
from firebase_admin import db, credentials
# from controllers.import_controllers import import_controllers  # done
# from sqlalchemy.exc import IntegrityError
from tools.password_encryption import encode_password
# from models.user import User
import uuid
import random
import os
import sys
from exceptions.basic_exception import BasicException


def create_app():
    app = Flask(__name__)

    cred = credentials.Certificate("localup-42a2d0b55f0b.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://localup-34dd4.firebaseio.com'
    })

    USERS = db.reference('users')
    SONGS = db.reference('songs')
    ARTISTS = db.reference('artists')
    SONGS = db.reference('songs')
    RADIOS = db.reference('radios')
    CONCERTS = db.reference('concerts')

    @app.route('/users/create', methods=['POST'])
    def create_user():
        req = request.json

        name = req["name"]
        email = req["email"]
        encoded_password = encode_password(req["password"])
        
        snapshot = USERS.order_by_child('email').equal_to(email).get()
        if snapshot:
            return jsonify({'message': 'Email Address Already Taken'}), 400

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

        if not snapshot:
            return jsonify({'message': 'Invalid Email'}), 400
        if retrieved_password != encoded_password:
            return jsonify({'message': 'Incorrect Password'}), 400
        return jsonify({'message': 'Success'}), 201

    @app.route('/artists/create', methods=['POST'])
    def create_artist():
        req = request.json

        name = req["name"]
        email = req["email"]
        bio = req["bio"]
        encoded_password = encode_password(req["password"])
        twitter = req["twitter"]
        insta = req["insta"]
        fb = req["fb"]
        
        snapshot = ARTISTS.order_by_child('email').equal_to(email).get()
        if snapshot:
            return jsonify({'message': 'Email Address Already Taken'}), 400

        artist = ARTISTS.push({
            'name': name,
            'email': email,
            'password': encoded_password,
            'bio': bio,
            'twitter' : twitter,
            'insta' : insta,
            'fb' : fb,
            'concert_ids': [""]
          });

        return jsonify({'id': artist.key}), 201


    @app.route('/artists/login', methods=['POST'])
    def login_artist():
        json = request.json
        email = json["email"]
        password = json["password"]
        encoded_password = encode_password(password)

        snapshot = ARTISTS.order_by_child('email').equal_to(email).get()
        for key, val in snapshot.items():
            retrieved_password = val['password']

        print(retrieved_password)
        print(encoded_password)
        if not snapshot:
            return jsonify({'message': 'Invalid Email'}), 400
        if retrieved_password != encoded_password:
            return jsonify({'message': 'Incorrect Password'}), 400
        return jsonify({'message': 'Success'}), 201


    @app.route('/songs/new', methods=['POST'])
    def new_song():
        req = request.json

        song_name = req["song_name"]
        artist = req["artist"]
        url = req["url"]
        genre = req["genre"]
        
        snapshot = SONGS.order_by_child('song_name').equal_to(song_name).get()
        if snapshot:
            return jsonify({'message': 'Song Name Already Taken'}), 400

        song = SONGS.push({
            'song_name': song_name,
            'artist': artist,
            'url': url,
            'genre': genre
          });

        return jsonify({'id': song.key}), 201

    @app.route('/radios/new', methods=['POST'])
    def create_radio():
        req = request.json

        city = req["city"]
        genres = req["genres"]
        songs = req["songs"]
        radio_name = req["radio_name"]
        
        snapshot = RADIOS.order_by_child('radio_name').equal_to(radio_name).get()
        if snapshot:
            return jsonify({'message': 'Radio Name Already Taken'}), 400

        radio = RADIOS.push({
            'city': city,
            'genres': genres,
            'songs': songs,
            'radio_name': radio_name
          });

        return jsonify({'id': radio.key}), 201


    @app.route('/radios/add_song', methods=['POST'])
    def add_song_to_radio():
        req = request.json 

        song_name = req["song_name"]
        radio_name = req["radio_name"]

        snapshot = RADIOS.order_by_child('radio_name').equal_to(radio_name).get()
        if not snapshot:
            return jsonify({'message': 'Invalid Radio Name'}), 400

        for key, val in snapshot.items():
            songs = val['songs']
            city = val['city']
            genres = val['genres']
            radio_name = val['radio_name']
            radio_id = key

        songs.append(song_name)

        radio_ref = RADIOS.child(radio_id)

        radio_ref.set({
            'city': city,
            'genres': genres,
            'songs': songs,
            'radio_name': radio_name
        })

        return jsonify({'message': 'Success'}), 201




    @app.route('/users/next_song', methods=['POST'])
    def random_song():
        req = request.json

        radio_name = req["radio_name"]

        snapshot = RADIOS.order_by_child('radio_name').equal_to(radio_name).get()
        if not snapshot:
            return jsonify({'message': 'Invalid Radio Name'}), 400

        for key, val in snapshot.items():
            songs = val['songs']

        # get random song from songs
        random_song = random.choice(songs)

        snapshot = SONGS.order_by_child('song_name').equal_to(random_song).get()
        for key, val in snapshot.items():
            url = val['url']

        return jsonify({'url': url}), 201


    @app.route('/artists/add_concert', methods=['POST'])
    def add_concert():
        req = request.json

        artist_name = req["artist_name"]
        dates = req["dates"]
        city = req["city"]

        concert_uuid = uuid.uuid4()
        concert_id = str(concert_uuid)


        snapshot = ARTISTS.order_by_child('name').equal_to(artist_name).get()
        if not snapshot:
            return jsonify({'message': 'Invalid Artist Name'}), 400

        for key, val in snapshot.items():
            artist_id = key
            email = val["email"]
            bio = val["bio"]
            encoded_password = val["password"]
            twitter = val['twitter']
            insta = val['insta']
            fb = val['fb']
            concert_ids = val['concert_ids']

        concert_ids.append(concert_id)
        concert_ids = list(filter(None, concert_ids))

        artist_ref = ARTISTS.child(artist_id)

        artist_ref.set({
            'name': artist_name,
            'email': email,
            'bio': bio,
            'password': encoded_password,
            'twitter': twitter,
            'insta': insta,
            'fb': fb,
            'concert_ids': concert_ids
        })

        concert = CONCERTS.push({
            'artist_name': artist_name,
            'dates': dates,
            'city': city,
            'concert_id': str(concert_id)
          });

        return jsonify({'id': concert.key}), 201

        


    # @app.route('/radio/new', methods=['POST'])
    # def create_radio():
    #     req = request.json

    #     #id = req["id"]
    #     genres = req["genres"]
    #     radio_name = req["radio_name"]
    #     user_email = req["user_email"]

    #     radio_id = uuid.uuid4()

    #     radio = RADIOS.push({
    #         'radio_id' : str(radio_id),
    #         'radio_name': radio_name,
    #         'user_email': user_email,
    #         'genres': genres
    #     });

    #     # RADIOS = USERS.child(id).child('radios')

    #     # radio_id = uuid.uuid4()

    #     # snapshot = RADIOS.order_by_child('radio_name').equal_to(radio_name).get()
    #     # if snapshot:
    #     #     return jsonify({'message': 'Radio Name Already Taken'}), 400

    #     # radio = RADIOS.push({
    #     #     'radio_id' : str(radio_id),
    #     #     'radio_name': radio_name,
    #     #     'genres': genres
    #     #   });

    #     #return jsonify({'message': 'Success'}), 201

    #     return jsonify({'id': radio.key}), 201
        

    # @app.route('/radio/get', methods=['POST'])
    # def get_radio()
    #     user_id = req["id"]



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