from flask import Flask,request
from os import path
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SESSION_PERMANENT'] = False

    from .views import views
    from .auth import auth
    active_connections = set()

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    @app.before_request
    def track_connection():
        active_connections.add(request.remote_addr)

    @app.teardown_request
    def check_disconnect(exception=None):
        if request.remote_addr in active_connections:
            active_connections.remove(request.remote_addr)
            if len(active_connections) == 0:
                # No active connections, stop the app
                shutdown_func = request.environ.get('werkzeug.server.shutdown')
                if shutdown_func is not None:
                    shutdown_func()

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
        # pass
        # return User.query.get(int(id))

    return app

