import telebot
import os
#from dotenv import load_dotenv
#load_dotenv(".env")


#____________Setting of bot__________________
bot = telebot.TeleBot(os.getenv("BOT_API"))
ADMIN_ID = os.getenv("ADMIN_ID")


@bot.message_handler(commands=['start'])
def start(message):
    """Sents start text when bot starts"""
    bot.send_message(message.chat.id, "Бот запущен!")

def support_message(text):
    """Resends Ideas from preposition to admin"""
    bot.send_message(ADMIN_ID, f"{text}")

if __name__ == "__main__":

    #___________Test___________
    support_message("Test")

    bot.infinity_polling()
    