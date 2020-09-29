from bot_answer import BotAnswer


class PasswordsBot:

    def get_answer(self, message):
        if message.text == '/start':
            return self.start_message()
        if message.text == '/check':
            return self.check_password_strength_welcome()
        if message.text == '/generate':
            return self.password_generation_variants()
        if message.text == '/recommendations':
            return self.recommendations()
        return BotAnswer('I don\'t understand you')

    def get_button_action_response(self, action, data):
        if action == 'generate':
            return self.password_generation_results(data)
        return BotAnswer('I don\'t understand you')

    def start_message(self):
        return BotAnswer('welcome message')

    def recommendations(self):
        return BotAnswer('InfoSec Recommendations')

    def password_generation_variants(self):
        # second parameter of bot answer should be a keyboard with possible generation variants
        # example - ({'text': 'RED', 'data': 'red button'}, {'text': 'BLUE', 'data': 'blue button'})
        # in data a string "generate <GENERATION METHOD>" should be passed ("generate abc")
        # it will be checked in the bot api to route to correct function (password generation)
        return BotAnswer('password generation variants with keyboard')

    def password_generation_results(self, method):
        return BotAnswer(f'list of generated passwords using method {method}')

    def check_password_strength_welcome(self):
        return BotAnswer('a request for user to enter a password to be checked')
