from flask import current_app, jsonify
import re


class Hangman:
    def __init__(self, id, word):
        self.id = id
        self.word = word
        self.separator = current_app.config['SEPARATOR']
        self.guess = self.separator * len(word)
        self.guesses = 0
        self.game_over = False

    def export_json(self):
        return jsonify({
            'id': self.id,
            'guess': self.guess,
            'guesses': self.guesses
        })

    def guess_letter(self, letter):
        if not self.game_over:
            if letter in self.guess:
                pass
            elif letter in self.word:
                indexes = [c.start() for c in re.finditer(letter, self.word)]
                for i in indexes:
                    self.guess = self.guess[:i] + letter + self.guess[i + 1:]
            else:
                self.guesses += 1
                if self.guesses >= 5:
                    self.game_over = True

    def is_game_over(self):
        return self.game_over
