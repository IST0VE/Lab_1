import telebot
import mysql.connector
import config
from mysql.connector import errorcode
from telebot import types

# Подключение к базе данных
try:
    cnx = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
)
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

# Создание бота
bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn_add = types.KeyboardButton('Добавить запись')
    edit_button = types.KeyboardButton(text="Редактировать запись")
    show_button = types.KeyboardButton(text="Показать мои записи")

    markup.add(edit_button, show_button, itembtn_add)
    bot.send_message(message.chat.id, 'Привет!', reply_markup=markup)
    
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

    insert_query = "INSERT INTO records (name, email, phone, telegram_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (name, email, phone, telegram_id))
    cnx.commit()

    bot.reply_to(message, 'Запись успешно добавлена!')

# Обработчик кнопки "Показать мои записи"
@bot.message_handler(func=lambda message: message.text == "Показать мои записи")
def show_records(message):
    user_id = message.from_user.id
    select_query = "SELECT id, name, email, phone FROM records WHERE telegram_id = %s"
    cursor.execute(select_query, (user_id,))
    result = cursor.fetchall()
    if result:
        bot.reply_to(message, "Вот ваши записи:")
        for row in result:
            record_id, name, email, phone = row
            record_text = f"ID: {record_id}\nИмя: {name}\nEmail: {email}\nТелефон: {phone}\n\n"
            bot.send_message(message.chat.id, record_text)
    else:
        bot.reply_to(message, "У вас нет записей.")

# Функция для редактирования записи в базе данных
def edit_record(message, record_id, name=None, email=None, phone=None):
  telegram_id = message.chat.id
  cursor = cnx.cursor()

  # Проверка, что пользователь имеет доступ к записи
  cursor.execute("SELECT id FROM records WHERE id = %s AND telegram_id = %s", (record_id, telegram_id))
  result = cursor.fetchone()

  if result is None:
    bot.send_message(telegram_id, "Вы не имеете доступа к этой записи.")
    return

  # Обновление полей записи в базе данных
  query = "UPDATE records SET "
  values = []
  if name is not None:
    query += "name = %s, "
    values.append(name)
  if email is not None:
    query += "email = %s, "
    values.append(email)
  if phone is not None:
    query += "phone = %s, "
    values.append(phone)
  query = query.rstrip(", ")
  query += " WHERE id = %s"
  values.append(record_id)
  cursor.execute(query, tuple(values))
  cnx.commit()

  bot.send_message(telegram_id, "Запись успешно изменена.")

# Обработка команды для редактирования записи
@bot.message_handler(commands=['edit'])
def handle_edit(message):
  args = message.text.split()[1:]
  record_id = args[0]
  name = None
  email = None
  phone = None
  if len(args) > 1:
    for arg in args[1:]:
      parts = arg.split("=")
      if parts[0] == "name":
        name = parts[1]
      elif parts[0] == "email":
        email = parts[1]
      elif parts[0] == "phone":
        phone = parts[1]
  edit_record(message, record_id, name, email, phone)

# Функция для удаления записи из базы данных
def delete_record(message, record_id):
  telegram_id = message.chat.id
  cursor = cnx.cursor()

  # Проверка, что пользователь имеет доступ к записи
  cursor.execute("SELECT id FROM records WHERE id = %s AND telegram_id = %s", (record_id, telegram_id))
  result = cursor.fetchone()

  if result is None:
    bot.send_message(telegram_id, "Вы не имеете доступа к этой записи.")
    return

  # Удаление записи из базы данных
  cursor.execute("DELETE FROM records WHERE id = %s", (record_id,))
  cnx.commit()

  bot.send_message(telegram_id, "Запись успешно удалена.")

# Обработка команды для удаления записи
@bot.message_handler(commands=['delete'])
def handle_delete(message):
  record_id = message.text.split()[1]
  delete_record(message, record_id)

bot.polling()

