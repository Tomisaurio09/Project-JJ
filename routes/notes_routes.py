from flask import Blueprint, request, jsonify, make_response
from models import Notes
from extensions import db
from pydantic import ValidationError
from validation import NotesSchema
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

# POST /notes – crear una nota.
# GET /notes – traer todas las notas del usuario.
# GET /notes/<id> – traer una nota específica.
# PUT /notes/<id> – actualizar una nota. vemos que carajo hago aca
# DELETE /notes/<id> – borrar una nota.

notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/notes", methods=["POST"])
@jwt_required
def create_notes():
    try:
        current_user_id = int(get_jwt_identity())
        note_data = request.get_json()
        valid_note = NotesSchema(**note_data).model_dump()
        new_note = Notes(
            user_id=current_user_id,
            title = valid_note["title"],
            content = valid_note["content"]
        )
        db.session.add(new_note)
        db.session.commit()
        return make_response("Note created succesfully", 201)
    except ValidationError as e:
        return f"Invalid data type, details: {e.errors()}",400
    
    except Exception as e:
        return f"An error in the server ocurred, details: {str(e)}",500

@notes_bp.route("/notes", methods=["GET"])
@jwt_required
def show_all_notes():
    current_user_id = int(get_jwt_identity())
    notes = Notes.query.filter_by(user_id=current_user_id).all()
    if not notes:
        return {"message" : "No notes found for this user"}, 404
    
    user_notes =[]

    for n in notes:
        user_notes.append({
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "created_at": n.created_at
        })

    return jsonify(user_notes)

@notes_bp.route("/notes/<id>", methods=["GET"])
@jwt_required
def show_one_note(id):
    note = Notes.query.filter_by(id=id).first()

    if not note:
        return jsonify({"error": "Note not found"}), 404
    
    note_data = {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at
    }

    return jsonify(note_data)
    

@notes_bp.route("/notes/<id>", methods=["DELETE"])
@jwt_required
def delete_note(id):
    note = Notes.query.get(id)

    if not note:
        return jsonify({"error": "Note not found"}), 404
    
    db.session.delete(note)
    db.session.commit
    return jsonify({"message": f"Note with ID {id} deleted successfully"}), 200

@notes_bp.route("/notes/<id>", methods=["PUT"])
@jwt_required()
def edit_note(id):
    try:
        current_user_id = int(get_jwt_identity())
        note = Notes.query.filter_by(id=id, user_id=current_user_id).first()

        if not note:
            return jsonify({"error": "Note not found"}), 404

        update_data = request.get_json()
        valid_data = NotesSchema(**update_data).model_dump()

        note.title = valid_data["title"]
        note.content = valid_data["content"]

        db.session.commit()

        return jsonify({"message": "Note updated successfully"}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500