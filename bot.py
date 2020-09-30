from bot_answer import BotAnswer


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
        return BotAnswer('InfoSec Recommendations')

    def password_generation_methods(self, length):
        # second parameter of bot answer should be a keyboard with possible generation variants
        # example - ({'text': 'RED', 'data': 'red button'}, {'text': 'BLUE', 'data': 'blue button'})
        # in data a string "generate_method <LENGTH> <METHOD>" should be passed ("generate 8 abc")
        # it will be checked in the bot api to route to correct function (password generation)
        #    generate 8 abc
        print("Length from previous step is " + length)
        return BotAnswer('available password generation methods variants with keyboard',
                         ({'text': 'symbols', 'data': f'generate {length} abc'},
                          {'text': 'numbers', 'data': f'generate {length} 123'}))

    def password_generation_length(self):
        # second parameter of bot answer should be a keyboard with possible generation variants
        # example - ({'text': 'RED', 'data': 'red button'}, {'text': 'BLUE', 'data': 'blue button'})
        # in data a string "generate_length <LENGTH>" should be passed ("generate_length 8")
        # it will be checked in the bot api to route to correct function (password generation)
        # 8 9 10 12 14 16 18 20
        # generate_length 8
        print()
        return BotAnswer('possible password generation lengths with keyboard',
                         ({'text': '8', 'data': 'generate_length 8'}, {'text': '9', 'data': 'generate_length 9'}))

    def password_generation_results(self, data):
        [length, method] = data.split(" ")
        return BotAnswer(f'list of generated passwords of length {length} using method {method}')

    def check_password_strength_welcome(self):
        return BotAnswer('a request for user to enter a password to be checked')
