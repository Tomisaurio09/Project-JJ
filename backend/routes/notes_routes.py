from flask import Blueprint, request, jsonify
from models.note import Notes
from models.folders import Folder
from extensions import db
from pydantic import ValidationError
from validation import NotesSchema, FolderSchema
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

@notes_bp.route("/create_folder", methods=["POST"])
@jwt_required()
def create_folder():
    current_user_id = int(get_jwt_identity()) #ya tengo el user id
    data = request.get_json() #solo pide un nombre para el folder
    name = data.get("name")

    if not name:
        return jsonify({"error": "Folder name is required"}), 400

    folder = Folder(name=name, user_id=current_user_id)
    db.session.add(folder)
    db.session.commit()

    return jsonify({"message": "Folder created", "folder_id": folder.id,"folder_name": folder.name})

@notes_bp.route("/folders", methods=["GET"])
@jwt_required()
def show_folders():
    user_id = int(get_jwt_identity())
    folders = Folder.query.filter_by(user_id=user_id).all()
    return jsonify([
        {"id": folder.id, "name": folder.name}
        for folder in folders
    ])

@notes_bp.route("/delete_folder/<id>", methods=["DELETE"])
@jwt_required()
def delete_folder(id):
    current_user_id = int(get_jwt_identity())
    folder = Folder.query.filter_by(id=id, user_id=current_user_id).first()
    if not folder:
        return jsonify({"error": "Folder not found"}), 404
    db.session.delete(folder)
    db.session.commit()
    return jsonify({"message": f"Folder with ID {id} deleted successfully"}), 200


@notes_bp.route("/edit_folder/<id>", methods=["PUT"])
@jwt_required()
def edit_folders(id):
    try:
        current_user_id = int(get_jwt_identity())
        folder = Folder.query.filter_by(id=id, user_id=current_user_id).first()

        if not folder:
            return jsonify({"error": "Folder not found"}), 404

        update_data = request.get_json()
        valid_data = FolderSchema(**update_data).model_dump()

        folder.name = valid_data["name"]

        db.session.commit()

        return jsonify({"message": "Folder updated successfully"}), 200
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
    

@notes_bp.route("/folders/<id>/notes", methods=["GET"])
@jwt_required()
def get_notes_in_folder(id):
    current_user_id = int(get_jwt_identity())
    notes = Notes.query.filter_by(user_id=current_user_id, folder_id=id).all()
    return jsonify([
        {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "created_at": n.created_at
        } for n in notes
    ])


@notes_bp.route("/create_note", methods=["POST"])
@jwt_required()
def create_notes():
    try:
        current_user_id = int(get_jwt_identity())
        note_data = request.get_json()
        valid_note = NotesSchema(**note_data).model_dump()
        
        folder_id = note_data.get("folder_id") #puede ser none
        if folder_id:
            folder = Folder.query.filter_by(id=folder_id, user_id=current_user_id).first()
            if not folder:
                return jsonify({"error": "Folder not found"}), 404

        new_note = Notes(
            user_id=current_user_id,
            title = valid_note["title"],
            content = valid_note["content"],
            folder_id=folder_id
        )
        db.session.add(new_note)
        db.session.commit()
        return jsonify({"message": "Note created succesfully"}), 201
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

@notes_bp.route("/show_notes", methods=["GET"])
@jwt_required()
def show_all_notes():
    current_user_id = int(get_jwt_identity())
    notes = Notes.query.filter_by(user_id=current_user_id).all()
    if not notes:
        return jsonify({"message" : "No notes found for this user"}), 404
    
    user_notes =[]

    for n in notes:
        user_notes.append({
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "created_at": n.created_at
        })

    return jsonify(user_notes)


@notes_bp.route("/delete_note/<id>", methods=["DELETE"])
@jwt_required()
def delete_note(id):
    note = Notes.query.get(id)

    if not note:
        return jsonify({"error": "Note not found"}), 404
    
    db.session.delete(note)
    db.session.commit
    return jsonify({"message": f"Note with ID {id} deleted successfully"}), 200

@notes_bp.route("/edit_note/<id>", methods=["PUT"])
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
        return jsonify({
            "error": "Invalid data type",
            "details": e.errors()
        }), 400

    except Exception as e:
        return jsonify({
            "error": "An error occurred on the server",
            "details": str(e)
        }), 500