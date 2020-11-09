import sqlite3
import telebot  # name of "pyTelegramBotAPI" for some reason
import datebase_functions_constructor as db


def get_text(all_message_text):
    try:
        command = all_message_text.split(' ', maxsplit=1)[1]
    except IndexError:
        command = None
    return command


def create_table(user_id):
    sql_request = db.form_request_new_table(user_id)
    curs.execute(sql_request)
    conn.commit()


token_file = open('token.txt', 'r')
bot = telebot.TeleBot(token_file.read())
token_file.close()

conn = sqlite3.connect("all_users.db", check_same_thread=False)
curs = conn.cursor()


@bot.message_handler(commands=['start', 'help'])
def start_help_handler(message):
    user_id = message.from_user.id

    def start_handler(message):
        bot.send_message(user_id, "Привет, " + message.from_user.username + "!")

    def help_handler(message):
        bot.send_message(user_id, "Я бот-планировщик задач. \n"
                                  "Я умею добавлять задачи: \n"
                                  "/new_item *задача* \n"
                                  "Показывать список активных задач: \n"
                                  "/all \n"
                                  "Удалять внесённые задачи: \n"
                                  "/delete *номер задачи* \n"
                                  "(номер задачи можно узнать, запросив список задач)")

    if message.text == '/start':
        start_handler(message)
    help_handler(message)


@bot.message_handler(commands=['new_item'])
def new_item_handler(message):
    text = get_text(message.text)
    user_id = message.from_user.id
    create_table(user_id)
    if text is None:
        bot.send_message(user_id, "Некорректное задание команды :( \n"
                                  "Пожалуйста, пишите всю команду в одно сообщение")
        return

    sql_request = db.form_request_add_task(user_id, text)
    curs.execute(sql_request)
    conn.commit()

    bot.send_message(user_id, "Задача \"" + text +
                     "\" успешно добавлена!")


@bot.message_handler(commands=['delete'])
def delete_handler(message):
    text = get_text(message.text)
    user_id = message.from_user.id
    create_table(user_id)
    if text is None:
        bot.send_message(user_id, "Некорректное задание команды :( \n"
                                  "Пожалуйста, пишите всю команду в одно сообщение")
        return

    try:
        task_number = int(text)
    except ValueError:
        bot.send_message(user_id, "Некорректное задание команды :( \n"
                                  "Кажется, номер удаляемой задачи не является целым числом")
        return

    try:
        sql_request = db.form_request_remember_deleted_task(user_id, task_number)
        deleted = curs.execute(sql_request).fetchall()[0][0]
        sql_request = db.form_request_delete_task(user_id, task_number)
        curs.execute(sql_request)
        conn.commit()
        bot.send_message(user_id, "Задача \"" + deleted + "\" успешно удалена!")
    except IndexError:
        bot.send_message(user_id, "Некорректное задание команды :( \n"
                                  "Кажется, не существует задачи под указаным номером")
        return


@bot.message_handler(commands=['all'])
def show_all_handler(message):
    user_id = message.from_user.id
    create_table(user_id)
    sql_request = db.form_request_count_elements_of_table(user_id)
    number_of_tasks = curs.execute(sql_request).fetchall()[0][0]

    if number_of_tasks == 0:
        bot.send_message(user_id, "Нет активных задач!")
    else:
        bot.send_message(user_id, "Список активных задач:")
        sql_request = db.form_request_show_all_tasks(user_id)
        for task in curs.execute(sql_request).fetchall():
            bot.send_message(user_id, str(task[0]) + ') ' + task[1])


@bot.message_handler(func=lambda m: True)
def all_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Извините, но я не понимаю :(")


bot.polling()

conn.close()
