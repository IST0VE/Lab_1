import telebot
import speech_recognition as sr
import config

# функция распознавания речи
def recognize_voice(filename):
    # создаем объект распознавания речи
    r = sr.Recognizer()

    # открываем голосовое сообщение
    with sr.AudioFile(filename) as source:
        audio = r.record(source)

    # распознаем речь с помощью Google Speech Recognition
    text = r.recognize_google(audio, language='ru-RU')

    # возвращаем расшифровку
    return text

# создаем объект бота и указываем токен
bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

# обрабатываем команду /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может расшифровывать голосовые сообщения. Просто отправь мне голосовое сообщение, и я попробую его расшифровать.")

# обрабатываем голосовое сообщение
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    # скачиваем голосовое сообщение
    voice_info = bot.get_file(message.voice.file_id)
    voice_file = bot.download_file(voice_info.file_path)

    # сохраняем голосовое сообщение на диск
    with open('voice.ogg', 'wb') as f:
        f.write(voice_file)

    # расшифровываем голосовое сообщение
    text = recognize_voice('voice.ogg')

    # отправляем расшифровку пользователю
    bot.reply_to(message, f"Расшифровка голосового сообщения: {text}")

# запускаем бота
bot.polling()
