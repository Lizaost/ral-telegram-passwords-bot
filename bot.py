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

    def start_message(self):
        return BotAnswer('welcome message')

    def recommendations(self):
        return BotAnswer('InfoSec Recommendations')

    def password_generation_variants(self):
        return BotAnswer('password generation variants with keyboard')

    def password_generation_results(self, method):
        return BotAnswer('list of generated passwords')

    def check_password_strength_welcome(self):
        return BotAnswer('a request for user to enter a password to be checked')