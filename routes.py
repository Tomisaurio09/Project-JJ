from flask import Blueprint, request, jsonify,jsonify, make_response
from models import User, Question
from extensions import db
from pydantic import ValidationError
from validation import UserSchema, LoginSchema, QuestionAnswerSchema

blueprint = Blueprint('api', __name__)

@blueprint.route("/register", methods=['POST'])
def register_user():
    try:
        data = request.get_json() #agarra la informacion del usuario
        user = (UserSchema(**data)) #crea una instancia del usuario y sus datos
        verified_user = user.model_dump()

        new_user = User(
            username=verified_user["username"],
            password=verified_user["password"]
        )

        db.session.add(new_user)
        db.session.commit()
        return make_response("User created successfully", 201)
    except ValidationError as e:
        return f"Invalid data type, details: {e.errors()}",400
    
    except Exception as e:
        return f"An error in the server ocurred, details: {str(e)}",500
    
@blueprint.route("/login", methods=["POST"])
def login_user():
    try:
        data_user = request.get_json()
        valid_user = LoginSchema(**data_user).model_dump()

        user = User.query.filter_by(username=valid_user["username"]).first()

        if user and user.password == valid_user["password"]:
            return make_response("Login successful", 200)
        else:
            return make_response("Invalid username or password",401)
    except ValidationError as e:
        return {"error":"Invalid input", "details": e.errors()},400
    
@blueprint.route("/question", methods=['POST'])
def question_user():
    try:
        question_data = request.get_json()
        valid_question = QuestionAnswerSchema(**question_data).model_dump()
        verified_question = Question(
            user_id=valid_question["user_id"],
            question_content=valid_question["question_content"],
            answer_content=valid_question["answer_content"]
        )
        db.session.add(verified_question)
        db.session.commit()
        return make_response("Question created succesfully",201)
    except ValidationError as e:
        return f"Invalid data type, details: {e.errors()}",400
    
    except Exception as e:
        return f"An error in the server ocurred, details: {str(e)}",500
    
@blueprint.route("/questions/<int:id_user>", methods=["GET"])
def get_user_questions(id_user):
    questions = Question.query.filter_by(user_id=id_user).all()
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