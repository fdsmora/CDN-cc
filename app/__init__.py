import os 

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import report
    app.register_blueprint(report.bp)

    swagger_url = '/api/docs'
    api_url = '/static/swagger.yml'
    swagger_blueprint = get_swaggerui_blueprint(
        swagger_url, 
        api_url,
    )
    app.register_blueprint(swagger_blueprint, url_prefix=swagger_url)

    # a simple page that says hello
    @app.route('/hello/')
    def hello():
        return 'Hello, World!'

    return app

class CDN_Request_Result_Type:
    HIT = 'Hit'
    MISS = 'Miss'
