from flask import Flask
from flask_autodoc import Autodoc
from hangman import Hangman
import random
from werkzeug import exceptions

app = Flask(__name__)
auto = Autodoc(app)

app.config.from_object('config')
WORDS = app.config['WORDS']
SEPARATOR = app.config['SEPARATOR']

list_games = []


@app.route('/guess/<game_id>/<letter>', methods=['POST'])
@auto.doc()
def guess(game_id, letter):
    '''Guesses a letter in the game_id game and returns its object'''

    if not game_id.isdigit() or len(letter) > 1:
        return exceptions.BadRequest()
    elif int(game_id) >= len(list_games):
        return exceptions.NotFound()

    game = list_games[int(id)]

    if game.is_game_over():
        return exceptions.NotAcceptable()
    game.guess_letter(letter)

    return game.export_json()


@app.route('/start', methods=['POST'])
@auto.doc()
def start():
    '''Creates a new game and returns its game_id'''

    # creating new game
    game = Hangman(id=len(list_games), word=WORDS[random.randint(0, len(WORDS) - 1)])
    list_games.append(game)

    return game.export_json()

@app.route('/documentation')
def documentation():
    return auto.html()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
