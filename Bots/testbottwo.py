import telebot
import mysql.connector
import config
from mysql.connector import errorcode

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
        print("Неверное имя пользователя или пароль")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("База данных не существует")
    else:
        print(err)

# Создание бота
bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    # Отправка пользователю сообщения со списком доступных команд
    commands_list = "/add - добавить новую запись\n/view - просмотреть список всех записей\n/edit - редактировать существующую запись\n/delete - удалить существующую запись"
    bot.send_message(message.chat.id, f"Доступные команды:\n{commands_list}")
    
# Обработчик команды /create
@bot.message_handler(commands=['create'])
def create_record(message):
    # Получение идентификатора пользователя и данных для создания новой записи
    user_id = message.chat.id
    chat_id = message.chat.id
    args = message.text.split()[1:]
    name = None
    email = None
    phone = None

    # Парсинг аргументов команды
    for arg in args:
        key, value = arg.split("=")
        if key == "name":
            name = value
        elif key == "email":
            email = value
        elif key == "phone":
           phone = value

    # Создание новой записи в базе данных
    query = "INSERT INTO records (user_id, name, email, phone) VALUES (%s, %s, %s, %s)"
    values = (user_id, name, email, phone)
    cursor.execute(query, values)
    cnx.commit()

    # Отправка сообщения пользователю об успешном создании записи
    bot.send_message(chat_id, "Запись успешно создана.")

# Обработчик команды /list
@bot.message_handler(commands=['list'])
def list_records(message):
    # Получение идентификатора пользователя для поиска записей в базе данных
    user_id = message.chat.id
    chat_id = message.chat.id

    # Поиск записей, созданных пользователем, в базе данных
    query = "SELECT * FROM records WHERE user_id = %s"
    values = (user_id,)
    cursor.execute(query, values)
    records = cursor.fetchall()

    # Отправка пользователю списка найденных записей
    if records:
        for record in records:
            # Форматирование строки с данными о записи
            text = f"ID: {record[0]}\nName: {record[2]}\nEmail: {record[3]}\nPhone: {record[4]}\n"
            bot.send_message(chat_id, text)
    else:
        bot.send_message(chat_id, "Записи не найдены.")

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

