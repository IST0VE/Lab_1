import telebot
from telebot import types
import mysql.connector
import config

# создаем бота и устанавливаем соединение с базой данных
bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
db = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
)
cursor = db.cursor()

@bot.message_handler(commands=['start'])
def start_handler(message):
    # Создание кнопок для выбора действия
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn_add = types.KeyboardButton('Добавить запись')

    markup.add(itembtn_add)

    bot.reply_to(message, 'Привет! Какую команду вы хотите выбрать?', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Добавить запись')
def add_record_handler(message):
    # Запрос имени
    bot.reply_to(message, 'Введите имя:')

    # Ожидание ответа с именем
    bot.register_next_step_handler(message, lambda msg: add_record_step2(msg, message.from_user.id))

def add_record_step2(message, telegram_id):
    # Сохранение имени
    name = message.text

    # Запрос email
    bot.reply_to(message, 'Введите email:')

    # Ожидание ответа с email
    bot.register_next_step_handler(message, lambda msg: add_record_step3(msg, telegram_id, name))

def add_record_step3(message, telegram_id, name):
    # Сохранение email
    email = message.text

    # Запрос телефона
    bot.reply_to(message, 'Введите телефон:')

    # Ожидание ответа с телефоном
    bot.register_next_step_handler(message, lambda msg: add_record_step4(msg, telegram_id, name, email))

def add_record_step4(message, telegram_id, name, email):
    # Сохранение телефона и запись в базу данных MySQL
    phone = message.text

    insert_query = "INSERT INTO records (name, email, phone, telegram-id) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (name, email, phone, telegram_id))
    db.commit()

    bot.reply_to(message, 'Запись успешно добавлена!')

bot.polling()
