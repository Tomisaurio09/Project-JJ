from flask import Blueprint, request, jsonify, make_response
from models import FillBlank
from extensions import db
from pydantic import ValidationError
from validation import FillBlankSchema
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

fillblank_bp =Blueprint('fillblank', __name__)

# POST /fillblanks
# GET /fillblanks
# DELETE /fillblanks/<id>

@fillblank_bp.route("/fillblanks", methods=["POST"])
@jwt_required
def post_sentence():
    try:
        current_user_id = int(get_jwt_identity())
        sentence_data = request.get_json()
        valid_sentence = FillBlankSchema(**sentence_data).model_dump()
        new_sentence = FillBlank(
            user_id=current_user_id,
            sentence=valid_sentence["sentence"],
            hidden_word=valid_sentence["hidden_word"]
        )
        db.session.add(new_sentence)
        db.session.commit()
        return make_response("Sentence created succesfully", 201)
    except ValidationError as e:
        return f"Invalid data type, details: {e.errors()}", 400
    
    except Exception as e:
        return f"An error in the server ocurred, details: {str(e)}",500

@fillblank_bp.route("/fillblanks", methods=["GET"])
@jwt_required
def get_sentences():
    current_user_id = int(get_jwt_identity())
    sentences = FillBlank.query.filter_by(user_id=current_user_id).all()
    if not sentences:
        return {"message": "No sentences found for this user"}, 404
    
    user_sentences = []

    for s in sentences:
        user_sentences.append({
            "id": s.id,
            "sentence": s.sentence,
            "hidden_word": s.hidden_word
        })

    return jsonify(user_sentences)

@fillblank_bp.route("/fillblanks/<int:id>", methods=["DELETE"])
@jwt_required
def delete_sentence(id):
    fill = FillBlank.query.get(id)

    if not fill:
        return jsonify({"error": "Fill-in-the-blank not found"}), 404
    
    db.session.delete(fill)
    db.session.commit()
    return jsonify({"message": f"Fill-in-the-blank with ID {id} deleted successfully"}), 200