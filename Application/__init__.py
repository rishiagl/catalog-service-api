from flask import Flask, jsonify

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    from . import db
    db.init_app(app)
    
    from Application.exception import InvalidAPIUsage
    
    @app.errorhandler(InvalidAPIUsage)
    def invalid_api_usage(e):
        return jsonify(e.to_dict()), e.status_code
    
    from Application import brand
    app.register_blueprint(brand.bp)
    
    from Application import brand_managers
    app.register_blueprint(brand_managers.bp)
    
    return app