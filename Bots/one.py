import openai
import telebot
import mysql.connector
import config

openai.api_key = config.OPENAI_TOKEN

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
conn = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
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

