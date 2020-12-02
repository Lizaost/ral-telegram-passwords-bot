import random
import hashlib
import requests
import json
import re

from bot_answer import BotAnswer
import random

SPECIALS = ['!', '@', '#', '$', '%', '^', '.', ',', '&', '*', '?', ':', ';', '+', '=']
NUMBERS = [str(x) for x in range(0, 10)]
LOWERCASE_LETTERS = [chr(x) for x in range(ord('a'), ord('z') + 1)]
UPPERCASE_LETTERS = [chr(x) for x in range(ord('A'), ord('Z') + 1)]


class PasswordsBot:

    def get_answer(self, message):
        if message.text == '/start':
            return self.start_message()
        if message.text == '/check':
            return self.check_password_strength_info()
        if message.text == '/generate':
            return self.password_generation_length()  # length -> methods -> results
        if message.text == '/recommendations':
            return self.recommendations()
        return self.check_password_strength(message.text)

    def get_button_action_response(self, action, data):
        if action == 'generate_length':
            return self.password_generation_methods(data)
        if action == 'generate':
            return self.password_generation_results(data)
        return BotAnswer('I don\'t understand you')

    def start_message(self):
        return BotAnswer(
            'Hi! I\'m RAL passwords bot and I can generate a password for you, check strength of your current '
            'password, and give you some information security recommendations. Use my commands /generate, /check '
            'and /recommendations, or send me your password and I will check if it is secure.')

    def recommendations(self):
        recommendations = [
            'Use different passwords for different services.',
            'Do not write down passwords, at least where someone else can read them. Its better to use a good '
            'passwords manager application.',
            'Do not share your passwords with anyone else.',
            'Use 2FA to make your accounts more secure.',
            'Use antivirus applications on your computer (and on mobile phone too).'
            'Do not download and open files from from unknown senders.',
            'Вo not follow the links in the letters without checking that it is in the right place.',
            'Enter your personal data only on sites in which you are sure. Before entering personal data, make sure '
            'that the site address in the address bar is correct (for example, google.com, not goggle.com).'
        ]
        message = 'I\'ve prepared some InfoSec recommendations for you.\n\n'
        for index, rec in enumerate(recommendations):
            message += f'{index + 1}. {rec}\n'
        return BotAnswer(message)

    def password_generation_methods(self, length):
        # second parameter of bot answer should be a keyboard with possible generation variants
        # example - ({'text': 'RED', 'data': 'red button'}, {'text': 'BLUE', 'data': 'blue button'})
        # in data a string "generate_method <LENGTH> <METHOD>" should be passed ("generate 8 abc")
        # it will be checked in the bot api to route to correct function (password generation)
        #    generate 8 abc
        print("Length from previous step: " + length)
        return BotAnswer('Select generation method',
                         ({'text': 'Lowercase letters', 'data': f'generate {length} a'},
                          {'text': 'Uppercase and lowercase letters', 'data': f'generate {length} Aa'},
                          {'text': 'Numbers', 'data': f'generate {length} 1'},
                          {'text': 'Letters and special symbols', 'data': f'generate {length} Aa!'},
                          {'text': 'Letters, numbers and special symbols', 'data': f'generate {length} Aa1!'},))

    def password_generation_length(self):
        # second parameter of bot answer should be a keyboard with possible generation variants
        # example - ({'text': 'RED', 'data': 'red button'}, {'text': 'BLUE', 'data': 'blue button'})
        # in data a string "generate_length <LENGTH>" should be passed ("generate_length 8")
        # it will be checked in the bot api to route to correct function (password generation)
        # 8 9 10 12 14 16 18 20
        # generate_length 8
        print()
        return BotAnswer('Select password length',
                         ({'text': '8', 'data': 'generate_length 8'},
                          {'text': '9', 'data': 'generate_length 9'},
                          {'text': '10', 'data': 'generate_length 10'},
                          {'text': '12', 'data': 'generate_length 12'},
                          {'text': '14', 'data': 'generate_length 14'},
                          {'text': '16', 'data': 'generate_length 16'},
                          {'text': '18', 'data': 'generate_length 18'},
                          {'text': '20', 'data': 'generate_length 20'},
                          ))

    def password_generation_results(self, data):
        [length, method] = data.split(" ")
        length = int(length)

        message = ""
        length = int(length)

        symbols_to_use = []
        password = []
        for c in method:
            if c == 'A':
                symbols_to_use.extend(UPPERCASE_LETTERS)
                password.append(random.choice(UPPERCASE_LETTERS)[0])
            elif c == 'a':
                symbols_to_use.extend(LOWERCASE_LETTERS)
                password.append(random.choice(LOWERCASE_LETTERS)[0])
            elif c == '1':
                symbols_to_use.extend(NUMBERS)
                password.append(random.choice(NUMBERS)[0])
            elif c == '!':
                symbols_to_use.extend(SPECIALS)
                password.append(random.choice(SPECIALS)[0])

        while len(password) < length:
            password.append(random.choice(symbols_to_use)[0])

        random.shuffle(password)
        password_string = ''.join(password)

        return BotAnswer(password_string)

    def check_password_strength_info(self):
        return BotAnswer(
            'Send me your password (ar a string with a similar structure which is better) and I will say how strong it is')

    def check_password_strength(self, password):

        # checking password strength

        score = 0
        message = ''

        # analyzing password's length
        if len(password) <= 6:
            pass
        elif len(password) <= 8:
            score += 1
        elif len(password) <= 10:
            score += 2
        elif len(password) <= 12:
            score += 3
        elif len(password) <= 14:
            score += 4
        else:
            score += 5

        # analyzing password's variety of symbols
        if re.search(r"[A-Z]", password):
            score += 1.5
        if re.search(r"[a-z]", password):
            score += 1.5
        if re.search(r"[0-9]", password):
            score += 1.5
        if re.search(r"[!@#$%^&*()№'+=]", password):
            score += 1.5

        # analyzing number of symbols repetitions
        repetitions = 0
        for i in range(1, len(password)):
            if password[i] == password[i - 1]: repetitions += 1

        if repetitions == 0:
            score += 2
        elif repetitions == 1:
            score += 1

        strengthes = {
            (0, 5): 'Your password is VERY WEAK.',
            (5, 7): 'Your password is WEAK.',
            (7, 9): 'Your password\'s strength is MEDIUM.',
            (9, 11): 'Your password is STRONG.',
            (11, 14): 'Your password is VERY STRONG.',
        }

        for (a, b), m in strengthes.items():
            if a <= score < b:
                message += m + "\n\n"

        # Checking if password is in leaked databases

        sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix = sha1_hash[:5:]
        suffix = sha1_hash[5::]
        res = requests.get('https://api.pwnedpasswords.com/range/' + prefix)
        # Have I been pwned API returns list of sha1 hashes suffixes
        # that have the same prefix that was passed as a GET query parameter
        # with number of occurrences of the hash in bases of hacked passwords.
        suffixes = list(map(lambda x: x.split(':')[0], res.text.split('\r\n')))
        is_pawned = suffix in suffixes
        message += 'WARNING! Your password is found in hacked password bases. ' \
                   'I recommend you to change it  as soon as possible.' if is_pawned \
            else 'Great! Your password is not in leaked passwords databases.'
        return BotAnswer(message)
