import random

from bot_answer import BotAnswer

SPECIALS = ['!', '@', '#', '$', '%', '^', '.', ',', '&', '*', '?', ':', ';', '+', '=']
NUMBERS = [str(x) for x in range(0, 10)]
LOWERCASE_LETTERS = [chr(x) for x in range(ord('a'), ord('z') + 1)]
UPPERCASE_LETTERS = [chr(x) for x in range(ord('A'), ord('Z') + 1)]


class PasswordsBot:

    def get_answer(self, message):
        if message.text == '/start':
            return self.start_message()
        if message.text == '/check':
            return self.check_password_strength_welcome()
        if message.text == '/generate':
            return self.password_generation_length()  # length -> methods -> results
        if message.text == '/recommendations':
            return self.recommendations()
        return BotAnswer('I don\'t understand you')

    def get_button_action_response(self, action, data):
        if action == 'generate_length':
            return self.password_generation_methods(data)
        if action == 'generate':
            return self.password_generation_results(data)
        return BotAnswer('I don\'t understand you')

    def start_message(self):
        return BotAnswer('welcome message')

    def recommendations(self):
        return BotAnswer('InfoSec Recommendations are not ready yet')

    def password_generation_methods(self, length):
        # second parameter of bot answer should be a keyboard with possible generation variants
        # example - ({'text': 'RED', 'data': 'red button'}, {'text': 'BLUE', 'data': 'blue button'})
        # in data a string "generate_method <LENGTH> <METHOD>" should be passed ("generate 8 abc")
        # it will be checked in the bot api to route to correct function (password generation)
        #    generate 8 abc
        print("Length from previous step is " + length)
        return BotAnswer('Select generation method',
                         ({'text': 'Lowercase letters', 'data': f'generate {length} a'},
                          {'text': 'Uppercase and lowercase letters', 'data': f'generate {length} Aa'},
                          {'text': 'numbers', 'data': f'generate {length} 1'},
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

        print(NUMBERS)
        print(LOWERCASE_LETTERS)
        print(UPPERCASE_LETTERS)

        message = ""

        symbols_to_use = []
        for c in method:
            if c == 'A':
                symbols_to_use.extend(UPPERCASE_LETTERS)
            elif c == 'a':
                symbols_to_use.extend(LOWERCASE_LETTERS)
            elif c == '1':
                symbols_to_use.extend(NUMBERS)
            elif c == '!':
                symbols_to_use.extend(SPECIALS)

        print(symbols_to_use)

        for i in range(1, 6):
            password = []
            for c in method:
                if c == 'A':
                    password.append(random.choice(UPPERCASE_LETTERS)[0])
                elif c == 'a':
                    password.append(random.choice(LOWERCASE_LETTERS)[0])
                elif c == '1':
                    password.append(random.choice(NUMBERS)[0])
                elif c == '!':
                    password.append(random.choice(SPECIALS)[0])

            while len(password) < length:
                password.append(random.choice(symbols_to_use)[0])

            random.shuffle(password)
            password_string = ''.join(password)
            message += f'{i}. {password_string}\n'

            print(password_string)

        return BotAnswer(message)

    def check_password_strength_welcome(self):
        return BotAnswer('Password\'s strength check is not ready yet')
