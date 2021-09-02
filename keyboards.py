from telebot import types


def admin_home_keyboard(username, chat_id):
    mark = types.InlineKeyboardMarkup
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton('income', callback_data="cb_income"),
                 types.InlineKeyboardButton('outcome', callback_data='cb_outcome'),
                 types.InlineKeyboardButton('search', callback_data='cb_search'),
                 types.InlineKeyboardButton('backup', callback_data='cb_backup'),
                 types.InlineKeyboardButton('reset', callback_data='cb_reset'),
                 types.InlineKeyboardButton('update', callback_data='cb_update'),
                 types.InlineKeyboardButton('history', callback_data='cb_history'), )
    return keyboard


def user_home_keyboard(username, chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton('user a', callback_data='cb_user_a'),
                 types.InlineKeyboardButton('user b', callback_data='cb_user_b'),
                 types.InlineKeyboardButton('banks', callback_data='cb_banks'))

    return keyboard


def update_keyboard(username, chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton('user a', callback_data='cb_update_user_a'),
                 types.InlineKeyboardButton('user b', callback_data='cb_update_user_b'),
                 types.InlineKeyboardButton('shekel bank', callback_data='cb_update_shekel_bank'),
                 types.InlineKeyboardButton('dollar bank', callback_data='cb_update_dollar_bank'))
    keyboard.add(types.InlineKeyboardButton('back', callback_data='cb_back_to_admin_home'))

    return keyboard


def banks_keyboard(username, chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton('shekel bank', callback_data='cb_shekel_bank'),
                 types.InlineKeyboardButton('dollar bank', callback_data='cb_shekel_bank'))
    return keyboard


def reset_keyboard(username, chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton('full reset', callback_data='cb_user_a'),
                 types.InlineKeyboardButton('half reset', callback_data='cb_user_b'),
                 types.InlineKeyboardButton('back', callback_data='cb_back_to_admin_home'))
    return keyboard


def back_keyboard(username, chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('back', callback_data='cb_back_to_admin_home'))
    return keyboard

