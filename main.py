import telebot
from telebot import types
import datetime
import sqlite3

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = telebot.TeleBot('6549394842:AAH6uK7zKiULJXDaXqH7onmZ1iedxH4Np4Y')

# Initialize the SQLite database



# Словарь аудиторий и поломок
auditoriums = ["Youtube", "Apple", "Viber", "Яндекс", "Авито", "VK", "Ebay", "Android", "Minecraft", "Tinkoff", "Future", "VR", "LG", "Linux", "HP", "Intel"]
problems = ["Не включается компьютер", "Нет изображения", "Нет интернета", "Нет нужной программы", "Wndows работает некорректно", "Мало памяти", "Не работает проектер/колонки", "Другое"]

# Переменные для хранения данных пользователя
user_auditorium = ""
user_problem = ""
user_name = ""

# Словарь для хранения запросов и времени
requests = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for auditorium in auditoriums:
        markup.add(types.KeyboardButton(auditorium))
    bot.send_message(message.chat.id, "В какой аудитории обнаружена поломка?", reply_markup=markup)
    bot.register_next_step_handler(message, get_auditorium)

# Обработчик выбора аудитории
def get_auditorium(message):
    global user_auditorium
    user_auditorium = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for problem in problems:
        markup.add(types.KeyboardButton(problem))
    bot.send_message(message.chat.id, "Что у вас сломалось?", reply_markup=markup)
    bot.register_next_step_handler(message, get_problem)

# Обработчик выбора поломки
def get_problem(message):
    global user_problem
    user_problem = message.text
    bot.send_message(message.chat.id, "Пожалуйста, введите ваше имя и фамилию:")
    bot.register_next_step_handler(message, get_name)

# Обработчик ввода имени
def get_name(message):
    global user_name
    user_name = message.text
    check_duplicate_request(message)

# Функция для проверки дубликатов запросов
def check_duplicate_request(message):
    global requests
    key = (user_auditorium, user_problem, user_name)
    if key in requests:
        # Если запрос с такими данными уже существует
        time_difference = datetime.datetime.now() - requests[key]
        if time_difference.total_seconds() < 4 * 3600:  # 4 часа в секундах
            bot.send_message(message.chat.id, "Вы уже отправили запрос.")
            return
    send_report(message)

# Отправка отчета
def send_report(message):
    conn = sqlite3.connect('requests.db')
    cursor = conn.cursor()
    global requests
    key = (user_auditorium, user_problem, user_name)
    requests[key] = datetime.datetime.now()
    report = f"Аудитория: {user_auditorium}\nПоломка: {user_problem}\nПользователь: {user_name}\nВремя отправки: {datetime.datetime.now()}"
    cursor.execute(f"INSERT INTO appeals (auditorium, problem, user_name, request_time) VALUES ('{user_auditorium}', '{user_problem}', '{user_name}', '{datetime.datetime.now()}')")
    conn.commit()
    bot.send_message(message.chat.id, report)
    start_over(message)


# Кнопка "Начать заново"
def start_over(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "Что бы вы хотели сделать дальше?", reply_markup=markup)
    bot.send_message(message.chat.id, "Для начала заново, отправьте команду /start")

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
