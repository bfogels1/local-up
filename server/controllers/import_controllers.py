def import_controllers(app):
    from controllers.users_controller import users_controller
    app.register_blueprint(users_controller, url_prefix="/users")
