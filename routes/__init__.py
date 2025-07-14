from .auth_routes import auth_bp
from .notes_routes import notes_bp
from .flashcard_routes import flashcard_bp
from .fillblank_routes import fillblank_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(flashcard_bp, url_prefix='/flashcards')
    app.register_blueprint(fillblank_bp, url_prefix='/fillblank')
