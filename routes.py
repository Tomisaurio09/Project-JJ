from flask import Blueprint, request, jsonify,jsonify, make_response, render_template
from models import User, Question
from extensions import db
from pydantic import ValidationError
from validation import UserSchema, LoginSchema, QuestionAnswerSchema
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

blueprint = Blueprint('api', __name__)

@blueprint.route("/")
def index():
    return render_template("index.html")



@blueprint.route("/register", methods=['POST'])
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
    
@blueprint.route("/login", methods=["POST"])
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

   
@blueprint.route("/question", methods=['POST'])
@jwt_required()
def question_user():
    try:
        current_user_id = int(get_jwt_identity())
        question_data = request.get_json()
        valid_question = QuestionAnswerSchema(**question_data).model_dump()
        new_question = Question(
            user_id=current_user_id,
            question_content=valid_question["question_content"],
            answer_content=valid_question["answer_content"]
        )
        db.session.add(new_question)
        db.session.commit()
        return make_response("Question created succesfully",201)
    except ValidationError as e:
        return f"Invalid data type, details: {e.errors()}",400
    
    except Exception as e:
        return f"An error in the server ocurred, details: {str(e)}",500
    
@blueprint.route("/questions", methods=["GET"])
@jwt_required()
def get_user_questions():
    current_user_id = int(get_jwt_identity())
    questions = Question.query.filter_by(user_id=current_user_id).all()
    if not questions:
        return {"message": "No questions found for this user"}, 404
    
    user_questions = []

    for q in questions:
        user_questions.append({
            "id": q.id,
            "question_content": q.question_content,
            "answer_content": q.answer_content
        })
    
    return jsonify(user_questions)


@blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = int(get_jwt_identity())
    new_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_token})