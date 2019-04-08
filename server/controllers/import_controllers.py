def import_controllers(app):
	from controllers.users_controller import users_controller
    app.register_blueprint(users_controller, url_prefix="/users")

    #from controllers.users_controller import users_controller
    #app.register_blueprint(users_controller, url_prefix="/users")

    #from controllers.events_controller import events_controller
    #app.register_blueprint(events_controller, url_prefix="/events")

    #from controllers.hosts_controller import hosts_controller
    #app.register_blueprint(hosts_controller, url_prefix="/hosts")

    #from controllers.spotify_controller import spotify_controller
    #app.register_blueprint(spotify_controller, url_prefix="/spotify")
