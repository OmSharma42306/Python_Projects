import telebot
Token="Your Token Number"

bot=telebot.TeleBot(Token)

@bot.message_handler(['start'])
def start(message):
    bot.reply_to(message,"Welcome To My BOT !")

@bot.message_handler(['about'])
def start(message):
    bot.reply_to(message,"This is A Bot! which you can make a simple Calculations here")

@bot.message_handler()
def sada(message):
    try: 
        msg=eval(message.text)
        
    except Exception as e:
            msg="Ida Calcualte AAgaangilla.."
    bot.reply_to(message,msg)
bot.polling()
