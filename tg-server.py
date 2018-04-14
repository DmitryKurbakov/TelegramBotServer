#! /usr/bin/env python
# -*- coding: utf-8 -*-


import telebot
from telebot import types
import dbtools
from flags import Flags
import helpers
import api

bot = telebot.TeleBot(api.tkey)

flags = Flags()


# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Search hackathons', callback_data='Search hackathons'))
    bot.send_message(message.chat.id, 'functionality', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def set_searching_type(call):
    if call.data == 'Search hackathons':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=search_by, callback_data=search_by) for search_by in
                       ['Title', 'Location', 'Type']])
        bot.send_message(chat_id=call.message.chat.id, text="Search by ...", reply_markup=keyboard)

    elif call.data == 'Title':
        flags.title= True
        bot.send_message(chat_id=call.message.chat.id, text="Input hackathon title")
    elif call.data == 'Location':
        flags.location = True
    elif call.data == 'Type':
        flags.type = True


@bot.message_handler(content_types=['text'])
def message_handler(m):
    if flags.title:
        res = dbtools.find_hackathons_by_title(m.text)

        bot.send_message(m.chat.id, helpers.form_message(res))
        flags.title = False


bot.polling(none_stop=True, interval=0)
