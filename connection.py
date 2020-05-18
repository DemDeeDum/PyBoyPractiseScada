import pymysql
import datetime
from datetime import timedelta 
import re
from contextlib import closing
from pymysql.cursors import DictCursor



def get_last_message():
    connection = pymysql.connect(
    host='localhost',
    user='root',
    password='narutoccc21',
    db='scadadb', 
    charset='utf8mb4', 
    cursorclass=DictCursor
    )
    try:
        with closing(connection.cursor()) as cursor:
       
            # SQL 
            sql = "select Text, Timestamp from scadadb.messages_data where Timestamp = (SELECT MAX(Timestamp) FROM scadadb.messages_data ) "

            cursor.execute(sql)
            res = cursor.fetchone()
            
            return "%s %s\n"%(res["Text"], res["Timestamp"].strftime("%Y-%m-%d %H:%M:%S"))
    except:
        return "Error"

def get_last_log():
    connection = pymysql.connect(
    host='localhost',
    user='root',
    password='narutoccc21',
    db='scadadb', 
    charset='utf8mb4', 
    cursorclass=DictCursor
    )
    try:
        with closing(connection.cursor()) as cursor:
       
            # SQL 
            sql = "select name, Value, Timestamp from scadadb.trends_data where Timestamp = (SELECT MAX(Timestamp) FROM scadadb.trends_data ) "

            cursor.execute(sql)
            res = cursor.fetchone()
            
            return ("Значение сборника <b>%s</b>: %s\nВремя: %s\n"
            %(res['name'], res["Value"], res["Timestamp"].strftime("%Y-%m-%d %H:%M:%S")))
    except:
        return "Error"

def get_messages_by_type(message_type):
    if message_type != -3 and message_type != -2 :
        return "Unexpected parameter"
    connection = pymysql.connect(
    host='localhost',
    user='root',
    password='narutoccc21',
    db='scadadb', 
    charset='utf8mb4', 
    cursorclass=DictCursor
    )
    try:
        
        with closing(connection.cursor()) as cursor:
       
            # SQL 
            sql = "select Text, Timestamp from (SELECT * FROM scadadb.messages_data ORDER BY Timestamp DESC) AS b where b.GroupID = %i limit 10"%(message_type)
            # Выполнить команду запроса (Execute Query).
            cursor.execute(sql)

            res = ""
            it = 1

            for row in cursor:
                res += "%i) %s <b>%s</b>\n"%(it, row["Text"], row["Timestamp"].strftime("%Y-%m-%d %H:%M:%S"))
                it = it + 1
            return res
    except:
        return "Error"

def get_objects_by_date(date_to_search, obj, select_mode) :
    str_to_query = check_and_get_new_datetime(date_to_search)
    if str_to_query == "Error" :
        return "Неверный формат даты!"
    connection = pymysql.connect(
    host='localhost',
    user='root',
    password='narutoccc21',
    db='scadadb', 
    charset='utf8mb4', 
    cursorclass=DictCursor
    )


    try :

        with closing(connection.cursor()) as cursor:
       
            # SQL 
            sql = ("select * from scadadb.%s where Timestamp > timestamp('%s') and Timestamp <= timestamp('%s') %s limit 30"
            %(obj, date_to_search, str_to_query.strftime("%Y-%m-%d %H:%M:%S"),
            "" if select_mode == "оба" else 'and name="%s"'%(select_mode)))
        
            # Выполнить команду запроса (Execute Query).
            cursor.execute(sql)
            res = ""
            it = 1
            if obj == 'trends_hour':
                prop = "Value"
            else :
                prop = "Text"

            for row in cursor:
                res += "%i) %s %s Время:<b>%s</b>\n"%(it, ("Сборник %s: "%(row['name']) if obj == 'trends_hour' else ""),
                row[prop], row["Timestamp"].strftime("%Y-%m-%d %H:%M:%S"))
                it = it + 1
            return res
    except :
        return "Неверный формат даты!"
             

def check_and_get_new_datetime(date_str):
    if(len(date_str) != 19) :
        return "Error"
    try:
        buf_date = date_str.split('-')
        item = buf_date[len(buf_date) - 1]
        buf_date.pop()
        buf_time = item.split(' ')
        buf_date.append(buf_time[0])
        buf_time.pop(0)
        buf_time = ''.join(buf_time).split(':')
        check = datetime.datetime(int(buf_date[0]), int(buf_date[1])
        , int(buf_date[2]), int(buf_time[0])
        , int(buf_time[1]), int(buf_time[2]))
        return check + timedelta(minutes=1)
    except:
        return "Error"



def get_average_value_by_date(initial_date, end_date, select_mode) :
    check_initial = check_and_get_new_datetime(initial_date)
    check_end = check_and_get_new_datetime(end_date)
    if check_initial == "Error" or check_end == "Error" :
        return "Неверный формат даты!"
    if check_initial > check_end :
        return "Начальная дата должна быть раньше конечной!"
    connection = pymysql.connect(
    host='localhost',
    user='root',
    password='narutoccc21',
    db='scadadb', 
    charset='utf8mb4', 
    cursorclass=DictCursor
    )


    try :

        with closing(connection.cursor()) as cursor:
       
            # SQL 
            sql = ("select AVG(Value) from scadadb.trends_hour where Timestamp > timestamp('%s') and Timestamp <= timestamp('%s') %s"
            %(initial_date, end_date,
            "" if select_mode == "оба" else 'and name="%s"'%(select_mode)))
        
            # Выполнить команду запроса (Execute Query).
            cursor.execute(sql)
            val = cursor.fetchone()['AVG(Value)']
            if val is None:
                return "На промежутке времени от %s до %s %s"%(
                    initial_date, end_date,
                    "не было найдено ни одного лога!"
                )

            return ('Среднее значение показателей %s равняется <b>%s</b>😇 %s%s'%(
                ("обеих сборников" if select_mode=="оба" else
                'сборника %s'%(select_mode))
                ,val,
                "\nВы можете узнать более подробную информацию используя",
                " команду /getLogsByTime !!"))
    except :
        return "Неверный формат даты!"
             
















myd = datetime.datetime.now()
lasthour = datetime.datetime(myd.year, myd.month , myd.day , myd.hour, myd.minute, myd.second)
print(lasthour.strftime("%Y-%m-%d %H:%M:%S"))
datead = datetime.datetime(2020,5,16,8,10,12)
if datead.strftime("%Y-%m-%d %H:%M:%S") == '2020-05-16 08:10:12':
    print("aaaa!")



def get_last_hour_messages():
    try:
  
        with connection.cursor() as cursor:
       
            # SQL 
            sql = "select Text from scadadb.messages_data where Timestamp > timestamp('%s')"%(datead.strftime("%Y-%m-%d %H:%M:%S"))
            # Выполнить команду запроса (Execute Query).
            cursor.execute(sql)
         
            print ("cursor.description: ", cursor.description)
 
            print()

            for row in cursor:
                print(row["Text"])
    except:
        return "Error"
             

def f():
    try:
  
        with connection.cursor() as cursor:
       
            # SQL 
            sql = "select * from scadadb.trends_day"
         
            # Выполнить команду запроса (Execute Query).
            cursor.execute(sql)
         
            print ("cursor.description: ", cursor.description)
 
            print()
    
        # for row in cursor:
            #print(row['Value'])
    except:
        return "Error"         