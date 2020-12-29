import telebot
from .config import Secrets
import datetime

secrets = Secrets()
bot = telebot.TeleBot(secrets["tg_token"])
chat_id = secrets["chat_id"]
boot_datetime = datetime.datetime.today()


def send_message(text):
    bot.send_message(chat_id, text)


def pretty_time_delta(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%dd%dh%dm%ds' % (days, hours, minutes, seconds)
    elif hours > 0:
        return '%dh%dm%ds' % (hours, minutes, seconds)
    elif minutes > 0:
        return '%dm%ds' % (minutes, seconds)
    else:
        return '%ds' % (seconds,)


@bot.message_handler(func=lambda message: message.chat.id == chat_id, commands=["check"])
def send_welcome(message):
    send_message("I'm alive!")


@bot.message_handler(func=lambda message: message.chat.id == chat_id, commands=["session"])
def send_welcome(message):
    delta = datetime.datetime.now() - boot_datetime
    text = f"Бот работает с {datetime.datetime.strftime(boot_datetime, '%H:%M %d/%m/%y')}\n" \
           f"На протяжении {pretty_time_delta(delta.total_seconds())}"
    send_message(text)


def startup():
    send_message("I'm alive again!")


# def single_poll():
#     print(1)
#     updates = bot.get_updates(offset=(bot.last_update_id + 1), timeout=20)
#     print(len(updates), updates)
#     bot.process_new_updates(updates)
#     print(2)
#     # bot.poll()


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=5)
