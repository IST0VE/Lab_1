import telebot
import datetime
import os

TOKEN = os.environ.get('6262622771:AAEbHR-8RlopH8O0OPx0dN6iO0JRt-gk7G0')
bot = telebot.TeleBot(TOKEN)

tasks = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот-планировщик задач. Чтобы запланировать задачу, отправь мне сообщение в следующем формате: /add Дата время Задача")

@bot.message_handler(commands=['add'])
def add_task(message):
    try:
        _, date, time, *task = message.text.split()
        dt = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
        tasks[message.chat.id] = {'datetime': dt, 'task': ' '.join(task)}
        bot.reply_to(message, f'Задача "{tasks[message.chat.id]["task"]}" добавлена на {dt}')
    except (ValueError, TypeError):
        bot.reply_to(message, 'Ошибка в формате. Введите дату и время в формате ГГГГ-ММ-ДД ЧЧ:ММ')
        
@bot.message_handler(commands=['list'])
def list_tasks(message):
    if message.chat.id in tasks:
        bot.reply_to(message, f'Ваши задачи: {tasks[message.chat.id]["task"]} на {tasks[message.chat.id]["datetime"]}')
    else:
        bot.reply_to(message, 'У вас нет запланированных задач.')
        
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, 'Неизвестная команда. Введите /help для получения справки.')

def check_tasks():
    while True:
        for chat_id in tasks:
            if datetime.datetime.now() >= tasks[chat_id]['datetime']:
                bot.send_message(chat_id, f'Напоминаю, у вас запланирована задача: "{tasks[chat_id]["task"]}" на {tasks[chat_id]["datetime"]}')
                del tasks[chat_id]
        time.sleep(60)

if __name__ == '__main__':
    import threading
    check_tasks_thread = threading.Thread(target=check_tasks)
    check_tasks_thread.start()
    bot.polling()
