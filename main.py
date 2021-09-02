import sqlite3
import src
from telebot import *
from dbhelper import DBHelper
from keyboards import *
import date

bot = telebot.TeleBot(src.TOKEN, parse_mode=None)
admins = [src.admin]
users = [src.user]
states = {"income": False, "outcome": False}
income_outcome_pattern = r'\d+\$?\,[\w \s]+\,[\w \s]+'
date_formats = ["%d-%m-%Y", "%d.%m.%Y", "%d/%m/%Y", "%d-%m-%y", "%d.%m.%y", "%d/%m/%y"]
messages_ids = []
db_path = 'cal.db'
db = DBHelper()

# Handlers


@bot.message_handler(content_types='text')
def handle_random_text(message):
    print(message.text)
    if message.text == '/start':
        send_welcome(message)
    else:
        msg = bot.send_message(message.from_user.id, 'invalid input')
        messages_ids.append(msg.message_id)
        messages_ids.append(message.message_id)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.delete_message(message.from_user.id, message.id)
    bot.send_photo(message.from_user.id, photo=open('images/zizo_logo.jpg', 'rb'), caption='welcome to zizo bot',
                   parse_mode='Markdown',
                   reply_markup=admin_home_keyboard(message.from_user.id
                                                    , message.id
                                                    ))


@bot.message_handler(regexp=income_outcome_pattern)
def handle_income_outcome_input(message):
    messages_ids.append(message.message_id)
    data = text_to_dict(message.text)
    print(threading.get_ident())
    data["date"] = str(date.get_now())
    if '$' in message.text:
        data["sum"] = data["sum"].replace('$', '')
        db.insert_col_data(data["sum"], data["description"], data["name"], data["date"], str(get_current_state(states)),
                           True)
    else:
        pass
        db.insert_col_data(data["sum"], data["description"], data["name"], data["date"], str(get_current_state(states)),
                           False)
    msg = bot.send_message(message.from_user.id, str(get_current_state(states)) + ' added')
    messages_ids.append(msg.message_id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'cb_income':
        states["income"] = True
        states["outcome"] = False
        caption = 'enter income in the next pattern\n amount,name,description '
        edit_caption_and_photo(call, 'images/Income.jpg', caption,
                               back_keyboard(call.from_user.username, call.from_user.id))
    elif call.data == 'cb_outcome':
        states["outcome"] = True
        states["income"] = False
        caption = 'enter income in the next pattern\n amount,name,description '
        edit_caption_and_photo(call, 'images/outcome.JPG', caption,
                               back_keyboard(call.from_user.username, call.from_user.id))
    elif call.data == 'cb_search':
        edit_caption_and_photo(call, 'images/search.png', 'search mode',
                               back_keyboard(call.from_user.username, call.from_user.id))
    elif call.data == 'cb_backup':
        edit_caption_and_photo(call, 'images/backup.png', 'backup mode',
                               back_keyboard(call.from_user.username, call.from_user.id))
    elif call.data == 'cb_reset':
        edit_caption_and_photo(call, 'images/reset.jpg', 'reset mode',
                               reset_keyboard(call.from_user.username, call.from_user.id))
    elif call.data == 'cb_update':
        edit_caption_and_photo(call, 'images/update.jpg', 'update mode',
                               back_keyboard(call.from_user.username, call.from_user.id))
    elif call.data == 'cb_history':
        edit_caption_and_photo(call, 'images/history.jpg', 'history mode',
                               back_keyboard(call.from_user.username, call.from_user.id))
    elif call.data == 'cb_back_to_admin_home':
        for message_id in messages_ids:
            bot.delete_message(call.from_user.id, message_id)
        messages_ids.clear()
        edit_caption_and_photo(call, 'images/zizo_logo.jpg', 'welcome to zizo bot',
                               admin_home_keyboard(call.from_user.username, call.from_user.id))


# Helpers
def get_current_state(dictionary):
    for key in dictionary.keys():
        if dictionary[key]:
            return key


def edit_caption_and_photo(call, img_src, caption, reply_markup):
    msg = bot.edit_message_media(
        media=types.InputMediaPhoto(open(img_src, 'rb')),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )
    print(msg)
    bot.edit_message_caption(chat_id=msg.chat.id, message_id=msg.message_id,
                             caption=caption,
                             reply_markup=reply_markup)


def text_to_dict(text):
    words = str.split(text, ",")
    words_dict = {
        "sum": words[0],
        "description": words[1],
        "name": words[2],
    }
    return words_dict


def main():
    print(threading.get_ident())
    db.setup()
    bot.polling()


if __name__ == '__main__':
    main()
