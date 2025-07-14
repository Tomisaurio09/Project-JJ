from flask import Flask
from extensions import db, migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()  # <-- Asegura que se cargue el .env
    app = Flask(__name__)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:KOBQSTPpjMGwNnTWboJGBSeIJYLHrFnk@trolley.proxy.rlwy.net:33788/railway"
    app.config['SECRET_KEY'] = 'una_clave_segura'
    app.config['JWT_SECRET_KEY'] = 'clave_super_secreta'
    jwt = JWTManager(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from routes import register_blueprints
    register_blueprints(app)
    
    return app
