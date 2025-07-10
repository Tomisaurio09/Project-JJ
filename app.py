from flask import Flask
from extensions import db, migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:TU_PASSWORD@containers-us-west-97.railway.app:3306/railway'

    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    from routes import blueprint
    app.register_blueprint(blueprint, url_prefix='/api')

    return app
