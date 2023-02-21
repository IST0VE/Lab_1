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
    bot.send_message(message.chat.id, 'Привет!')

# Обработчик текстового сообщения с id пользователя
@bot.message_handler(func=lambda message: True)
def edit_record(message):
    telegram_id = message.from_user.id
    # Поиск пользователя по id в базе данных
    cursor.execute("SELECT * FROM records WHERE telegram_id=%s", (telegram_id,))
    user = cursor.fetchone()

    if not user:
        # Если пользователь не найден, выводим сообщение об ошибке
        bot.send_message(message.chat.id, 'Пользователь с таким id не найден!')
    else:
        # Если пользователь найден, выводим кнопки для редактирования записи
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton('Изменить имя', callback_data='name'))
        markup.row(telebot.types.InlineKeyboardButton('Изменить email', callback_data='email'))
        markup.row(telebot.types.InlineKeyboardButton('Изменить телефон', callback_data='phone'))
        markup.row(telebot.types.InlineKeyboardButton('Изменить все', callback_data='all'))
        bot.send_message(message.chat.id, f'Выбери, что нужно изменить для пользователя {user[1]} ({user[2]}, {user[3]})', reply_markup=markup)

        # Обработчик нажатия на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    telegram_id = call.message.text.split()[4]  # Получаем id пользователя из сообщения
    field = call.data  # Получаем название поля, которое нужно изменить

    if field == 'all':
        # Если пользователь выбрал "Изменить все", выводим соответствующее сообщение
        bot.send_message(call.message.chat.id, 'Отправь мне новые данные через одно сообщение в формате "Имя Фамилия, email, телефон"')
    else:
        # Если пользователь выбрал изменить конкретное поле, выводим соответствующее сообщение
        bot.send_message(call.message.chat.id, f'Отправь мне новое значение для поля "{field}"')

    # Регистрируем следующий обработчик
    bot.register_next_step_handler(call.message, lambda message: update_record(message, telegram_id, field))

# Обработчик сообщения с новыми данными пользователя
def update_record(message, telegram_id, field):
    new_value = message.text.strip()
    update_query = ''
    telegram_id = message.from_user.id
    # Проверяем, существует ли пользователь с заданным id в базе данных
    #cursor.execute('SELECT * FROM records WHERE telegram_id=%s', (telegram_id,))
    result = cursor.fetchone()

    if not result:
        # Если пользователь не найден, выводим сообщение об ошибке
        bot.send_message(message.chat.id, 'Пользователь с таким id не найден в базе данных')
        return

    if field == 'name':
        # Изменяем имя пользователя
        update_query = "UPDATE records SET name=%s WHERE telegram_id=%s"
    elif field == 'email':
        # Изменяем email пользователя
        update_query = "UPDATE records SET email=%s WHERE telegram_id=%s"
    elif field == 'phone':
        # Изменяем телефон пользователя
        update_query = "UPDATE records SET phone=%s WHERE telegram_id=%s"
    elif field == 'all':
        # Изменяем все поля пользователя
        new_values = new_value.split(',')
        if len(new_values) != 3:
            # Если количество полей не равно 3, выводим сообщение об ошибке
            bot.send_message(message.chat.id, 'Неверный формат данных. Попробуй еще раз.')
            return
        name, email, phone = [value.strip() for value in new_values]
        update_query = "UPDATE records SET name=%s, email=%s, phone=%s WHERE telegram_id=%s"

    # Обновляем данные пользователя в базе данных
    try:
        if field == 'name':
            cursor.execute(update_query, (new_value, telegram_id))
        elif field == 'email':
            cursor.execute(update_query, (new_value, telegram_id))
        elif field == 'phone':
            cursor.execute(update_query, (new_value, telegram_id))
        elif field == 'all':
            cursor.execute(update_query, (name, email, phone, telegram_id))
        cnx.commit()
        bot.send_message(message.chat.id, 'Запись успешно изменена!')
    except mysql.connector.Error as error:
        print("Ошибка при обновлении записи: {}".format(error))
        cnx.rollback()
        bot.send_message(message.chat.id, 'Произошла ошибка при изменении записи. Попробуйте еще раз.')

bot.polling(none_stop=True)
 

bot.polling()