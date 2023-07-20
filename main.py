import telebot
import time
from multiprocessing import *
import schedule
import random
import io
import os
from os.path import join, dirname
from dotenv import load_dotenv
from telebot import types
def get_from_env(key):
    dotenv_path = join(dirname(__file__), 'token.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)
token = get_from_env('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(token)


def start_process():  # Запуск Process
    p1 = Process(target=P_schedule.start_schedule, args=()).start()


class P_schedule():  # Class для работы с schedule
    def start_schedule():  # Запуск schedule
        ######Параметры для schedule######
        schedule.every().day.at("12:00").do(P_schedule.send_message1)
        ##################################

        while True:  # Запуск цикла
            schedule.run_pending()
            time.sleep(1)

    def send_message1():
        fileObj = io.open('text.txt', "r", encoding='utf-8')  # opens the file in read mode
        words = fileObj.read().splitlines()  # puts the file into an array
        fileObj.close()
        texttosend = random.choice (words)
        with open('id.txt', 'r') as f:
            for line in f:
                try:
                    bot.send_message(line, texttosend)
                except:
                    print ('отписался')
###Настройки команд telebot#########
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    back = types.KeyboardButton('/tip')
    markup.add(back)
    bot.send_message(message.chat.id, 'Привет, я бот который будет поддерживать и подбадривать тебя ежедневно! Надеюсь я тебе хоть немного помогу\nКаждый день в 12:00 по времени моего создателя я буду присылать вам сообщение\nСпасибо что подписались', reply_markup=markup)
    fileObj = io.open('text.txt', "r", encoding='utf-8')  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    texttosend = random.choice(words)
    bot.send_message(message.chat.id, f'Вот сегодняшнее сообщение для тебя: {texttosend}')
    with open("id.txt", "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(f"{message.chat.id}")
@bot.message_handler(commands=['tip'])
def tip(message):
    bot.send_message(message.chat.id, 'If you wanna tip me - https://www.buymeacoffee.com//wolfhoundt6')
#####################


if __name__ == '__main__':
    start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass