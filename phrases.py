option_logs_by_date = "/getLogsByTime - вывести логи по дате"
option_message_by_date = "/getMessagesByTime - вывести сообщения по дате"
option_all_autorise_messages = "/getLastAuthoriseMessages - вывести последние сообщения авторизации"
option_all_warning_messages = "/getLastWarningMessages - вывести последние сообщения тревоги" 
option_average_by_dates = "/getAverageValueByDates - вывести среднее значение показателей сборников по времени"
add_info = "Возможен вывод лишь 30 записей одновременно😔"

def _greeting():
    return 'Приветствую тебя!\nЯ бот,созданный для опроса базы данных <b>SCADA-системы</b>'
def _options():
    return (
        'С помощью меня вы можете:\n' +
        option_logs_by_date + "\n" +
        option_message_by_date + "\n" +
        option_all_autorise_messages + "\n" +
        option_all_warning_messages + "\n" +
        option_average_by_dates + "\n\n" +
        add_info + "\n"
        )

def _date_input_instruction():
    return """
Введите дату и время используя следующий формат:\n
"год-месяц-день час:минута:секунда"\n
Если в номере месяца или дня будут значения меньше 10 напишите перед числом 0😉
\n2020-05-01 04:04:04 - первое мая четыре часа четыре минуты четыре секунды утра😊
\nБудут выведены данные в промежутке <b>ОДНОЙ</b> минуты начиная с введенного вами времени
    """

def _select_instruction() :
    return """
Отлично, теперь выберите сборник, логи о котором, вы хотите посмотреть/рассчитать.
\nВы можете выбрать как сборники А и B вместе, так и по отдельности 😉
    """

def _get_date_format_input_error():
    return """
Вы неправильно ввели дату😔
Или же были введены несуществующие номера дней, часов или минут🤔
    """

def _range_choice_instruct_initial():
    return """
Итак для начала выберите начальную дату!
"""

def _range_choice_instruct_end():
    return """
Отлично😇, теперь точно также выберем конечную!
"""