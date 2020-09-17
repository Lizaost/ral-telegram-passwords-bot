import os
import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(f'Received message {message}')
    send_message(message.from_user.id, "TEST REPLY FROM BOT")
    send_message_with_keyboard(message.from_user.id,
                               'Test message with keyboard',
                               ({'text': 'RED', 'data': 'red button'},
                                {'text': 'BLUE', 'data': 'blue button'})
                               )


@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call):
    print(call)


def send_message(user_id, text):
    bot.send_message(user_id, text)


# keyboard_structure = ({'text': 'BUTTON', 'data':'data'}, ...)
def send_message_with_keyboard(user_id, text, keyboard_structure):
    keyboard = types.InlineKeyboardMarkup()
    for button in keyboard_structure:
        key = types.InlineKeyboardButton(text=button['text'], callback_data=button['data'])
        keyboard.add(key)
    bot.send_message(user_id, text=text, reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
