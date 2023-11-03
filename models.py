from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor_username = db.Column(db.String(80))
    guesser_username = db.Column(db.String(80))
    word_to_guess = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=False)
