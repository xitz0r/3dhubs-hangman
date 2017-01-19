from flask import Flask, jsonify
import random
import re
from werkzeug import exceptions

app = Flask(__name__)

app.config.from_object('config')
WORDS = app.config['WORDS']

dict_games = {}
counter = 0


def destroy_game(id):
    dict_games.pop(int(id))


# exports only selected fields
def game_export(game):
    return jsonify({'id': game['id'], 'guess': game['guess'], 'guesses': game['guesses']})


@app.route('/guess/<id>/<letter>')
def guess(id, letter):
    if not id.isdigit() or len(letter) > 1 or not letter.isalpha():
        return exceptions.BadRequest()
    elif int(id) not in dict_games.keys():
        return exceptions.NotFound()

    game = dict_games[int(id)]
    word = game['word']

    if letter in game['guess']:
        pass
    elif letter in word:
        indexes = [c.start() for c in re.finditer(letter, word)]
        guess = game['guess']
        for i in indexes:
            guess = guess[:i] + letter + guess[i + 1:]
        game['guess'] = guess

        if '_' not in guess:
            destroy_game(int(id))
    else:
        game['guesses'] += 1
        if game['guesses'] >= 5:
            destroy_game(int(id))
            return exceptions.NotAcceptable()

    return game_export(game)


@app.route('/start')
def start():
    global counter  # it seems by default flask is single threaded, so this won't be a problem

    word = WORDS[random.randint(0, len(WORDS) - 1)]
    game = {
        'id': counter,
        'word': word,
        'guess': '_' * len(word),
        'guesses': 0
    }

    dict_games[counter] = game
    counter += 1

    return game_export(game)


if __name__ == '__main__':
    app.run()
