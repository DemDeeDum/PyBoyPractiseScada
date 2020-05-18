import telebot
import config
import connection
import phrases 
import random
import keyboards
from telebot import types

class FlagSet:
    def __init__(self):
        self.date_input_mode = False
        self.message_date_mode = False
        self.log_date_mode = False
        self.select_mode = "оба"
        self.end_date = "None"
        self.initial_date = ""


flags = FlagSet()
bot = telebot.TeleBot(config.TOKEN)
help = "/help - вывести команды еще раз"

@bot.message_handler(commands=['start'])
def greeting(message):
    sti = open('static/Greeting.tgs', 'rb')
    _to_user =  '<b>%s!</b>'%(message.from_user.first_name)
    bot.send_sticker(message.chat.id, sti)
    msg = '%s\n%s\n%s\n%s'%(_to_user, phrases._greeting(), phrases._options(), help)
    bot.send_message(message.chat.id, msg ,parse_mode='html',
    reply_markup=keyboards.main_markup)

@bot.message_handler(commands=['help'])
def options(message):
    sti = open('static/Thinking.tgs', 'rb')
    _to_user =  '<b>%s!</b>'%(message.from_user.first_name)
    bot.send_sticker(message.chat.id, sti)
    msg = '%s\n%s\n%s'%(_to_user, phrases._options(), help)
    bot.send_message(message.chat.id, msg ,parse_mode='html',
    reply_markup=keyboards.main_markup)


@bot.message_handler(commands=['getLastAuthoriseMessages'])
def getAutoriseMessages(message):
    _to_user = '<b>Сообщения авторизации для %s!</b>'%(message.from_user.first_name)
    sti = open('static/Kiss.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    msg = '%s\n%s\n%s'%(_to_user, connection.get_messages_by_type(-3), help)
    bot.send_message(message.chat.id, msg ,parse_mode='html',
    reply_markup=keyboards.main_markup)

@bot.message_handler(commands=['getLastWarningMessages'])
def getWarningMessages(message):
    _to_user = '<b>Сообщения тревоги для %s!</b>'%(message.from_user.first_name)
    sti = open('static/Warning.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    msg = '%s\n%s\n%s'%(_to_user, connection.get_messages_by_type(-2), help)
    bot.send_message(message.chat.id, msg ,parse_mode='html',
    reply_markup=keyboards.main_markup)

@bot.message_handler(commands=['getMessagesByTime'])
def getWarningMessagesByDate(message):
    _to_user = '<b>%s!</b>'%(message.from_user.first_name) 
    msg = '%s %s'%(_to_user, phrases._date_input_instruction())
    bot.send_message(message.chat.id, msg ,parse_mode='html',
    reply_markup=keyboards.main_menu())
    flags.date_input_mode = True
    flags.message_date_mode = True

@bot.message_handler(commands=['getLogsByTime'])
def getWarningMessagesByDate(message):
    _to_user = '<b>%s!</b>'%(message.from_user.first_name)
    msg = '%s %s'%(_to_user, phrases._select_instruction())
    bot.send_message(message.chat.id, msg ,parse_mode='html',
    reply_markup=keyboards.select_menu())
    flags.log_date_mode = True

@bot.message_handler(commands=['getAverageValueByDates'])
def getAverageValueByDates(message):
    _to_user = '<b>%s!</b>'%(message.from_user.first_name)
    msg = '%s %s'%(_to_user, phrases._select_instruction())
    bot.send_message(message.chat.id, msg ,parse_mode='html',
    reply_markup=keyboards.select_menu())
    flags.end_date = "Waiting for choice"


@bot.callback_query_handler(func=lambda call: True)
def getInlineMenuValues(call):
    if True:
        if call.message:
            if call.data == "A" or call.data == "B" or call.data == "оба":
                bot.edit_message_text(chat_id=call.message.chat.id
                    , message_id=call.message.message_id,
                    text='Отлично!Выбор сделан😊',
                    reply_markup=None)
                flags.select_mode = call.data
                _to_user = '<b>%s!</b>'%(call.message.chat.first_name)
                choice = "Вы выбрали %s!"%(flags.select_mode)
                if flags.log_date_mode:
                    msg = '%s %s %s'%(_to_user, choice, phrases._date_input_instruction())
                    bot.send_message(call.message.chat.id, msg ,parse_mode='html',
                    reply_markup=keyboards.main_menu())
                    flags.date_input_mode = True
                elif flags.end_date == "Waiting for choice":
                    msg = '%s %s %s %s'%(_to_user, choice,
                     phrases._range_choice_instruct_initial(),
                     phrases._date_input_instruction())
                    bot.send_message(call.message.chat.id, msg ,parse_mode='html',
                    reply_markup=keyboards.main_menu())
                    flags.end_date = "Waiting for initial"


    else:
        print("Error")

@bot.message_handler(content_types=['text'])
def handler(message):
    if message.chat.type == 'private':
        if flags.end_date == "Waiting for initial":
            getSecondDate(message)
        elif flags.end_date == "Waiting for end":
            getAverageValue(message)
        elif flags.date_input_mode:
            answerObjectsByDate(message)
        elif message.text == '🎱 случайное число':
            bot.send_message(message.chat.id,'Ваше случайное число - %i😘\n\n%s'%(random.randint(0,100),help))
        elif message.text == '📩 последнее сообщение':
            bot.send_message(message.chat.id,"😉\n%s\n%s"%(connection.get_last_message()
            , help), parse_mode='html')
        elif message.text == '📈 последний лог':
            bot.send_message(message.chat.id, '😊\n%s\n%s'%(connection.get_last_log(), help)
            , parse_mode='html')
        else :
            bot.send_message(message.chat.id, 'Сообщение %s не является командой' % (message.text))
    else :
        bot.send_message(message.chat.id, 'Я так не работаю!!!')

def getSecondDate(message):
    if connection.check_and_get_new_datetime(message.text) == "Error":
        flags.end_date = "None"
        bot.send_message(message.chat.id, phrases._get_date_format_input_error())
        return
    bot.send_message(message.chat.id, phrases._range_choice_instruct_end())
    flags.end_date = "Waiting for end"
    flags.initial_date = message.text

def getAverageValue(message):
    _to_user = "Результат для <b>%s!</b>"%(
        message.from_user.first_name
    )
    res = connection.get_average_value_by_date(
        flags.initial_date
    , message.text
    , flags.select_mode)
    msg = '%s %s\n\n%s'%(_to_user, res, help)
    bot.send_message(message.chat.id, msg ,parse_mode='html',
    reply_markup=keyboards.main_markup)
    flags.end_date = "None"
    flags.initial_date = ""

def answerObjectsByDate(message) :
    res = connection.get_objects_by_date(
    message.text.strip(), 
    'messages_data'if flags.message_date_mode else 'trends_hour',
    flags.select_mode)
    if res == "Неверный формат даты!" or res == "":
        if res == "":
            res = "Ничего не найдено :-("
        _to_user = '<b>К сожалению мы не получили желаемые вами данные %s!</b>'%(message.from_user.first_name)
        sti = open('static/SAD.tgs', 'rb')
    else :
        _to_user ='<b>Сообщения по времени для ' if flags.message_date_mode else '<b>Логи по времени для '
        _to_user += '%s!</b>'%(message.from_user.first_name)
        sti = open(
            ('static/MesByDate.tgs'if flags.message_date_mode else 'static/LogByDate.tgs')
            , 'rb')
                    
    bot.send_sticker(message.chat.id, sti)
    msg = '%s\n%s\n\n%s'%(_to_user, res, help)
    bot.send_message(message.chat.id, msg ,parse_mode='html',
        reply_markup=keyboards.main_menu())
    flags.date_input_mode = False
    flags.message_date_mode = False
    flags.log_date_mode = False
    flags.select_mode = "оба"

#RUN
bot.polling(none_stop=True)