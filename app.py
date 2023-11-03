from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Game

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        game = Game.query.first()
        if not game:
            game = Game()
            db.session.add(game)
        if role == 'Actor' and not game.actor_username:
            game.actor_username = username
        elif role == 'Guesser' and not game.guesser_username:
            game.guesser_username = username
        else:
            flash('Role is already taken', 'error')
            return render_template('login.html')
        db.session.commit()
        return redirect(url_for('game', username=username, role=role))
    return render_template('login.html')

@app.route('/game/<username>/<role>')
def game(username, role):
    game = Game.query.first()
    if not game:
        flash('No active game', 'error')
        return redirect(url_for('login'))
    if role == 'Actor' and game.actor_username == username:
        return render_template('actor.html', username=username, game=game)
    elif role == 'Guesser' and game.guesser_username == username:
        return render_template('guesser.html', username=username, game=game)
    else:
        flash('Invalid role or username', 'error')
        return redirect(url_for('login'))

@app.route('/start_game', methods=['POST'])
def start_game():
    game = Game.query.first()
    if game and game.actor_username and game.guesser_username:
        game.is_active = True
        db.session.commit()
        return redirect(url_for('game', username=game.actor_username, role='Actor'))
    flash('Game cannot be started', 'error')
    return redirect(url_for('login'))

@app.route('/select_word', methods=['POST'])
def select_word():
    word = request.form['word']
    game = Game.query.first()
    if game:
        game.word_to_guess = word
        db.session.commit()
        return redirect(url_for('game', username=game.actor_username, role='Actor'))
    return "No active game", 404

@app.route('/guess', methods=['POST'])
def guess():
    guess = request.form['guess']
    game = Game.query.first()
    if game and game.word_to_guess:
        # TODO: Check the guess against the word_to_guess and update game state
        pass  # Placeholder
    return redirect(url_for('game', username=game.guesser_username, role='Guesser'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
