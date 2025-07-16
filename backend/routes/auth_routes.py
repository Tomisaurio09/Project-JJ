from flask import Blueprint, request, jsonify, render_template
from models.user import User
from extensions import db
from pydantic import ValidationError
from validation import UserSchema, LoginSchema
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

#Login system

@auth_bp.route("/register", methods=['POST'])
def register_user():
    try:
        data = request.get_json() #agarra la informacion del usuario
        user = UserSchema(**data).model_dump() #crea una instancia del usuario y sus datos

        #verifica si el usuario ya existe en la database
        if User.query.filter_by(username=user["username"]).first():
            return jsonify({"error": "Username already exists"}), 400
        
        #hashea la contraseña del usuario
        hashed_password = generate_password_hash(user["password"])
        new_user = User(username=user["username"], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(message="User created successfully"), 201
    except ValidationError as e:
        return f"Invalid data type, details: {e.errors()}",400
    
    except Exception as e:
        return f"An error in the server ocurred, details: {str(e)}",500

    
@auth_bp.route("/login", methods=["POST"])
def login_user():
    try:
        data_user = request.get_json()
        valid_user = LoginSchema(**data_user).model_dump()

        #como los username son unicos, aca obtiene uno solo, el cual es una "fila" de la base de datos
        user = User.query.filter_by(username=valid_user["username"]).first() 
        if user and check_password_hash(user.password, valid_user["password"]):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            return jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        return jsonify({"error": "Invalid username or password"}), 401
    except ValidationError as e:
        return {"error":"Invalid input", "details": e.errors()},400


