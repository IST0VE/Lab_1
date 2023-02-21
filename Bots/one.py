import openai
import telebot
import mysql.connector

# Initialize the OpenAI API client with your API key
openai.api_key = "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"

# Initialize the Telegram bot with your bot token
bot = telebot.TeleBot("6262622771:AAEbHR-8RlopH8O0OPx0dN6iO0JRt-gk7G0")

conn = mysql.connector.connect(
    host="mysql.j98515082.myjino.ru",
    user="j98515082",
    password="HiuhasUH83",
    database="j98515082_test"
)

# Define a function to generate a text response using the OpenAI GPT-3 model
def generate_response(text):
    prompt = f"Q: {text}\nA:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=2,
        stop=None,
        temperature=0.75,
    )
    return response.choices[0].text.strip()

# Define a handler for incoming messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text
    created_at = message.date
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (user_id, message, created_at) VALUES (%s, %s, %s)", (user_id, text, created_at))
    conn.commit()
    text = message.text
    response = generate_response(text)
    bot.reply_to(message, response)

# Start the bot
bot.polling()

