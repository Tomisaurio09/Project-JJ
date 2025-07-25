from flask import Blueprint, request, jsonify
from models.flashcard import Flashcard
from extensions import db
from pydantic import ValidationError
from validation import FlashCardSchema
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

flashcard_bp = Blueprint('flashcards', __name__)

#Flashcards system
@flashcard_bp.route("/create_question", methods=['POST'])
@jwt_required()
def question_user():
    try:
        current_user_id = int(get_jwt_identity())
        question_data = request.get_json()
        valid_question = FlashCardSchema(**question_data).model_dump()
        new_question = Flashcard(
            user_id=current_user_id,
            question_content=valid_question["question_content"],
            answer_content=valid_question["answer_content"]
        )
        db.session.add(new_question)
        db.session.commit()
        return jsonify({"message": "Question created succesfully"}),201
    except ValidationError as e:
        return jsonify({
            "error": "Invalid data type",
            "details": e.errors()
        }), 400

    except Exception as e:
        return jsonify({
            "error": "An error occurred on the server",
            "details": str(e)
        }), 500
    
@flashcard_bp.route("/show_questions", methods=["GET"])
@jwt_required()
def show_user_questions():
    current_user_id = int(get_jwt_identity())
    questions = Flashcard.query.filter_by(user_id=current_user_id).all()
    if not questions:
        return jsonify({"message": "No questions found for this user"}), 404
    
    user_questions = []

    for q in questions:
        user_questions.append({
            "id": q.id,
            "question_content": q.question_content,
            "answer_content": q.answer_content
        })
    
    return jsonify(user_questions)

@flashcard_bp.route("/delete_question/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_question(id):
    flashcard = Flashcard.query.get(id)

    if not flashcard:
        return jsonify({"error": "Flashcard not found"}), 404
    
    db.session.delete(flashcard)
    db.session.commit()
    return jsonify({"message": f"Flashcard with ID {id} deleted successfully"}), 200