import telebot
from telebot import types

main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
rand = types.KeyboardButton("🎱 случайное число")
last_message = types.KeyboardButton("📩 последнее сообщение")
last_log = types.KeyboardButton("📈 последний лог")
main_markup.add(rand, last_message, last_log)

def main_menu() :
    return main_markup

select_inline_markup = types.InlineKeyboardMarkup(row_width=3)
Achoice = types.InlineKeyboardButton("🅰️", callback_data = "A")
Bchoice = types.InlineKeyboardButton("🅱️", callback_data = "B")
Both = types.InlineKeyboardButton("🆎", callback_data = "оба")

select_inline_markup.add(Achoice, Bchoice, Both)

def select_menu() :
    return select_inline_markup