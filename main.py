import telebot
import sqlite3
import tracemalloc

tracemalloc.start()

db_path = 'db/movies.db'
token = "5815871684:AAE6LK8RoxA99kBMx6eys3mt3qx1bpXrncE"
bot = telebot.TeleBot(token)
array = ['919709921', '1106429047', '740834733', '998440931', '1907186997']


@bot.message_handler(commands=['start'])
def start_message(message):
    username = message.from_user.username
    bot.send_message(message.chat.id, "Привет @{0}! Скиньте код фильма чтобы узнать его название!".format(username))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    userid = message.from_user.id
    if str(userid) in array and "/111" in message.text:
        try:
            mess = message.text.split('\n')
            del mess[0]
            add_movie(mess)
        except Exception as e:
            bot.reply_to(message, f"Error: {e}\nОшибка\nФормат написание:" + """
/111
код фильма
название
ссылка""")

        return
    try:
        add_user(userid)
        result = get_movie_by_code(message.text)
        if result is not None:
            bot.reply_to(message, f"Название по коду {message.text}:  {result[0]} \nСсылка: {result[1]}")
        else:
            bot.reply_to(message, f"Несуществующий код")
    except sqlite3.OperationalError as e:
        add_user(userid)
        bot.reply_to(message, f"Несуществующий код")


def get_movie_by_code(code):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM movies WHERE id = {code}")

    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if result is not None:
        return result[1], result[2]
    else:
        raise sqlite3.OperationalError()


def add_movie(mess):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO movies (id, name, link) VALUES ({mess[0]}, '{mess[1]}', '{mess[2]}')")
    conn.commit()
    cursor.close()
    conn.close()


def add_user(userid):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (id) VALUES ({userid})")
    conn.commit()
    cursor.close()
    conn.close()


bot.infinity_polling()
