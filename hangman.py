from flask import current_app, jsonify
import re


class Hangman:
    def __init__(self, id, word):
        self.id = id
        self.word = word
        self.separator = current_app.config['SEPARATOR']
        self.guess = self.separator * len(word)
        self.wrong_guesses = 0
        self.wrong_letters = []
        self.game_over = False
        self.game_status = 'ongoing'

    def export_json(self):
        return jsonify({
            'id': self.id,
            'guess': self.guess,
            'wrong_guesses': self.wrong_guesses,
            'wrong_letters': self.wrong_letters,
            'game_status': self.game_status
        })

    def guess_letter(self, letter):
        if not self.game_over:
            if letter in self.guess or letter in self.wrong_letters:
                pass
            elif letter in self.word:
                indexes = [c.start() for c in re.finditer(letter, self.word)]
                for i in indexes:
                    self.guess = self.guess[:i] + letter + self.guess[i + 1:]
                if self.separator not in self.guess:
                    self.game_over = True
                    self.game_status = 'game won'
            else:
                self.wrong_guesses += 1
                self.wrong_letters.append(letter)
                if self.wrong_guesses >= 5:
                    self.game_over = True
                    self.game_status = 'game lost'

    def is_game_over(self):
        return self.game_over
