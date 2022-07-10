from aiogram import types


def creator_markup():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add('Order development🦾')
    return markup
