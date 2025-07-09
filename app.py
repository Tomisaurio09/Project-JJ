from flask import Flask
from extensions import db, migrate

def create_app():
    app = Flask('__name__')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'thisisthesecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    
    db.init_app(app)
    migrate.init_app(app, db)

    from routes import blueprint
    app.register_blueprint(blueprint, url_prefix='/api')
    
    return app




