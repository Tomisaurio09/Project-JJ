from flask import Flask
from extensions import db, migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta

def create_app():
    app = Flask('__name__')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'thisisthesecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config["JWT_SECRET_KEY"] = "clave_super_secreta"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from routes import blueprint
    app.register_blueprint(blueprint, url_prefix='/api')
    
    return app




