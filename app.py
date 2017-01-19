from flask import Flask, jsonify
import random

app = Flask(__name__)

app.config.from_object('config')
WORDS = app.config['WORDS']

dict_games = {}
counter = 0


# exports only selected fields
def game_export(game):
    return {'id': game['id'], 'guess': game['guess']}


@app.route('/start')
def start():
    global counter  # it seems by default flask is single threaded, so this won't be a problem

    word = WORDS[random.randint(0, len(WORDS) - 1)]
    game = {
        'id': counter,
        'word': word,
        'guess': '_' * len(word)
    }

    dict_games[counter] = game
    counter += 1

    return jsonify(game_export(game))


if __name__ == '__main__':
    app.run()
