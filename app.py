from flask import Flask
from hangman import Hangman
import random
from werkzeug import exceptions

app = Flask(__name__)

app.config.from_object('config')
WORDS = app.config['WORDS']
SEPARATOR = app.config['SEPARATOR']

list_games = []


@app.route('/guess/<id>/<letter>', methods=['POST'])
def guess(id, letter):
    if not id.isdigit() or len(letter) > 1:
        return exceptions.BadRequest()
    elif int(id) >= len(list_games):
        return exceptions.NotFound()

    game = list_games[int(id)]

    if game.is_game_over():
        return exceptions.NotAcceptable()
    game.guess_letter(letter)

    return game.export_json()


@app.route('/start', methods=['POST'])
def start():
    # creating new game
    game = Hangman(id=len(list_games), word=WORDS[random.randint(0, len(WORDS) - 1)])
    list_games.append(game)

    return game.export_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
