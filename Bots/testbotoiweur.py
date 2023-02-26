import mysql.connector
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import config

# Подключение к БД
db = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
)

# Инициализация бота
bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Отправка приветственного сообщения и кнопок
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(KeyboardButton('Показать все записи'), KeyboardButton('Добавить новую запись'))
    markup.add(KeyboardButton('Редактировать запись'), KeyboardButton('Удалить запись'))
    bot.reply_to(message, "Добро пожаловать! Выберите действие:", reply_markup=markup)

# Обработчик сообщения с новыми данными пользователя
@bot.message_handler(func=lambda message: message.text == 'Редактировать запись')
def edit_record(message):
    user_id = message.from_user.id
    record_id = message.text.split()[1] if len(message.text.split()) > 1 else None
    cursor = db.cursor()
    select_query = "SELECT * FROM records WHERE id = %s AND telegram_id = %s"
    cursor.execute(select_query, (record_id, user_id))
    record = cursor.fetchone()

    if record is None:
        bot.send_message(chat_id=user_id, text="Ошибка: запись не найдена или не принадлежит Вам")
    else:
        # Отправляем пользователю сообщение с текущими данными записи
        current_data = f"Текущие данные записи:\nИмя: {record[2]}\nEmail: {record[3]}\nТелефон: {record[4]}"
        bot.send_message(chat_id=user_id, text=current_data)

        # Отправляем пользователю запрос на ввод новых данных
        new_data = "Введите новые данные в формате: Имя Email Телефон"
        bot.send_message(chat_id=user_id, text=new_data)

        # Создаем клавиатуру с кнопками для подтверждения или отмены операции
        confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить", callback_data=f"confirm_edit_{record_id}")],
            [InlineKeyboardButton(text="Отмена", callback_data=f"cancel_edit_{record_id}")]
        ])

        # Отправляем клавиатуру пользователю
        bot.send_message(chat_id=user_id, text="Вы уверены, что хотите изменить запись?", reply_markup=confirm_keyboard)

# Обработчик команды "Показать все записи"
@bot.message_handler(func=lambda message: message.text == 'Показать все записи')
def show_records(message):
    user_id = message.from_user.id
    select_query = "SELECT * FROM records WHERE telegram_id = %s"
    cursor = db.cursor()
    cursor.execute(select_query, (user_id,))
    records = cursor.fetchall()
    if len(records) == 0:
        bot.reply_to(message, "У вас пока нет записей.")
    else:
        for record in records:
            bot.reply_to(message, f"ID: {record[0]}\nИмя: {record[1]}\nEmail: {record[2]}\nТелефон: {record[3]}")

# Обработчик команды "Добавить новую запись"
@bot.message_handler(func=lambda message: message.text == 'Добавить новую запись')
def add_record(message):
    user_id = message.from_user.id
    name = message.text.split()[1] if len(message.text.split()) > 1 else None
    email = message.text.split()[2] if len(message.text.split()) > 2 else None
    phone = message.text.split()[3] if len(message.text.split()) > 3 else None
    # Проверяем, что были указаны все необходимые поля
    if name is None or email is None or phone is None:
        bot.send_message(chat_id=user_id, text="Ошибка: необходимо указать имя, электронную почту и номер телефона")
        return
    else:
        # Добавляем новую запись в базу данных
        cursor = db.cursor()
        insert_query = "INSERT INTO records (telegram_id, name, email, phone) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (user_id, name, email, phone))
        db.commit()

        # Выводим сообщение об успешном добавлении записи
        bot.send_message(chat_id=user_id, text=f"Запись успешно добавлена: {name}, {email}, {phone}")

# Обработчик команды "Удалить запись"
@bot.message_handler(func=lambda message: message.text == 'Удалить запись')
def delete_record(message):
    
    user_id = message.from_user.id
    cursor = db.cursor()
    # Получаем список записей, принадлежащих пользователю
    select_query = "SELECT * FROM records WHERE telegram_id = %s"
    cursor.execute(select_query, (user_id,))
    records = cursor.fetchall()

    if not records:
        # Если записей нет, выводим сообщение об ошибке
        bot.send_message(chat_id=user_id, text="У Вас нет записей для удаления")
    else:
        # Создаем InlineKeyboardMarkup с кнопками для удаления каждой записи
        keyboard = [[InlineKeyboardButton(record[1], callback_data=f"delete_{record[0]}")] for record in records]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Выводим сообщение с кнопками и клавиатурой
        bot.send_message(chat_id=user_id, text="Выберите запись для удаления", reply_markup=reply_markup)

# Обработчик нажатия кнопки для удаления записи
@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_"))
def delete_record_callback(update, context):
    cursor = db.cursor()
    # Получаем id записи для удаления из callback_data
    record_id = update.callback_query.data.split("_")[1]

    # Получаем id пользователя, который отправил запрос на удаление записи
    user_id = update.callback_query.from_user.id

    # Получаем запись из базы данных, если ее не существует, то выводим сообщение об ошибке
    select_query = "SELECT * FROM records WHERE id = %s AND telegram_id = %s"
    cursor.execute(select_query, (record_id, user_id))
    record = cursor.fetchone()

    if record is None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ошибка: запись не найдена или не принадлежит Вам")
    else:
        # Удаляем запись из базы данных
        delete_query = "DELETE FROM records WHERE id = %s"
        cursor.execute(delete_query, (record_id,))
        db.commit()

        # Выводим сообщение об успешном удалении записи
        context.bot.send_message(chat_id=update.effective_chat.id, text="Запись успешно удалена")

        # Отправляем новый список записей с клавиатурой
        select_query = "SELECT * FROM records WHERE telegram_id = %s"
        cursor.execute(select_query, (user_id,))
        records = cursor.fetchall()

        if not records:
            context.bot.send_message(chat_id=user_id, text="У Вас пока нет записей")
        else:
            for record in records:
                markup = delete_record_buttons(record)
                context.bot.send_message(chat_id=user_id, text=f"{record[1]}, {record[2]}, {record[3]}", reply_markup=markup)

        # Отвечаем на callback_query, чтобы убрать клавиатуру с кнопками
        updater.dispatcher.add_handler(CallbackQueryHandler(delete_record_callback, pass_user_data=True))


def delete_record_buttons(record):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Удалить", callback_data=f"delete_{record[0]}"))
    return markup

bot.polling()


