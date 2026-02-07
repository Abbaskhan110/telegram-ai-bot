import telebot
import requests
from gtts import gTTS

BOT_TOKEN = "8539966919:AAGHXOUp-HuXw7Ueta7I-KCsmCrqgGtkGWg"
GROQ_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)

def ask_ai(text):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system",
             "content": "You are Abbas AI assistant. Talk in Hinglish short replies."},
            {"role": "user", "content": text}
        ]
    }

    r = requests.post(url, headers=headers, json=data)
    return r.json()["choices"][0]["message"]["content"]


@bot.message_handler(func=lambda m: True)
def handle(message):

    reply = ask_ai(message.text)

    tts = gTTS(reply, lang='en')
    tts.save("reply.mp3")

    bot.send_voice(message.chat.id, open("reply.mp3", "rb"))


bot.polling()
