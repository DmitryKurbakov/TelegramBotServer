#! /usr/bin/env python
# -*- coding: utf-8 -*-


import telebot
from telebot import types
import dbtools
from flags import Flags
import helpers
import api
import time
from datetime import datetime

bot = telebot.TeleBot(api.tkey)

flags = Flags()


def every_day(message):
    result = dbtools.get_hackathons_in_week()
    if len(result) > 0:
        output_message_after_search_process(result, message.chat.id, message)
    else:
        bot.send_message(message.chat.id, text="in week hackathons will not be held =(")
    time.sleep(3)


# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text=relevance, callback_data=relevance) for relevance in
                   ['Upcoming', 'Past', 'All']])
    bot.send_message(message.chat.id, 'Please choose the list of hackathon you are interested in:', reply_markup=keyboard)

    # while True:
    #     now = datetime.now()
    #     if now.hour == 20 and now.minute == 00 and now.second == 0:
    #         every_day(message)


def output_message_after_search_process(res, chat, m):
    if res.__len__() != 0:
        if res.__len__() > 5:
            i = 0
            t = []
            while i < res.__len__():
                if i == 20:
                    break
                t.append(res[i])
                if i % 5 == 0:
                    bot.send_message(chat, helpers.form_message(t))
                    time.sleep(0.5)
                    t = []
                i += 1
        else:
            bot.send_message(chat, helpers.form_message(res))
    else:
        bot.send_message(chat, text="I did not find the hackathons according to the specified parameters")
    handle_start_help(m)


@bot.callback_query_handler(func=lambda call: True)
def set_searching_type(call):
    db_types = dbtools.get_hackathon_types()
    if call.data == 'Upcoming':
        flags.upcoming_hackathons = True
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=functionality, callback_data=functionality) for functionality in
                       ['Show', 'Search']])
        bot.send_message(chat_id=call.message.chat.id, text="Please choose the following step:", reply_markup=keyboard)
    elif call.data == 'Past':
        flags.past_hackathons = True
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=functionality, callback_data=functionality) for functionality in
                       ['Show', 'Search']])
        bot.send_message(chat_id=call.message.chat.id, text="Please choose the following step:", reply_markup=keyboard)
    elif call.data == 'All':
        flags.all_hackathons = True
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=functionality, callback_data=functionality) for functionality in
                       ['Show', 'Search']])
        bot.send_message(chat_id=call.message.chat.id, text="Please choose the following step:", reply_markup=keyboard)

    elif call.data == 'Show':
        if flags.upcoming_hackathons:
            res = dbtools.get_hackathons_by_relevance(0)
            output_message_after_search_process(res, call.message.chat.id, call.message)
            flags.upcoming_hackathons = False
        elif flags.past_hackathons:
            res = dbtools.get_hackathons_by_relevance(1)
            output_message_after_search_process(res, call.message.chat.id, call.message)
            flags.past_hackathons = False
        elif flags.all_hackathons:
            res = dbtools.get_hackathons_by_relevance(2)
            output_message_after_search_process(res, call.message.chat.id, call.message)
            flags.all_hackathons = False

    elif call.data == 'Search':
        flags.search_hackathons = True
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=search_by, callback_data=search_by) for search_by in
                       ['Title', 'Location', 'Type']])
        bot.send_message(chat_id=call.message.chat.id, text="Search by", reply_markup=keyboard)

    elif call.data == 'Title':
        flags.title = True
        bot.send_message(chat_id=call.message.chat.id, text="Input title of hackathon:")
    elif call.data == 'Location':
        flags.location = True
        bot.send_message(chat_id=call.message.chat.id, text="Input location of hackathon:")
    elif call.data == 'Type':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=db_type, callback_data=db_type) for db_type in db_types])
        flags.type = True
        bot.send_message(chat_id=call.message.chat.id, text="Choose type of hackathon:", reply_markup=keyboard)

    elif flags.type:
        res = []
        if flags.upcoming_hackathons:
            res = dbtools.get_hackathons_by_relevance(0)
            flags.upcoming_hackathons = False
        elif flags.past_hackathons:
            res = dbtools.get_hackathons_by_relevance(1)
            flags.past_hackathons = False
        elif flags.all_hackathons:
            res = dbtools.get_hackathons_by_relevance(2)
            flags.all_hackathons = False

        db_types = dbtools.get_hackathon_types()
        for db_type in db_types:
            if call.data == db_type:
                res = helpers.find_hackathons_by_type(db_type, res)
                output_message_after_search_process(res, call.message.chat.id, call.message)
                flags.type = False
                break


@bot.message_handler(content_types=['text'])
def message_handler(m):
    res = []
    if flags.upcoming_hackathons:
        res = dbtools.get_hackathons_by_relevance(0)
        flags.upcoming_hackathons = False
    elif flags.past_hackathons:
        res = dbtools.get_hackathons_by_relevance(1)
        flags.past_hackathons = False
    elif flags.all_hackathons:
        res = dbtools.get_hackathons_by_relevance(2)
        flags.all_hackathons = False

    if flags.title:
        res = helpers.find_hackathons_by_title(m.text, res)
        output_message_after_search_process(res, m.chat.id, m)
        flags.title = False
    elif flags.location:
        new_res = helpers.find_hackathons_by_country(m.text, res)
        if new_res.__len__() == 0:
            new_res = helpers.find_hackathons_by_location(m.text, res)
        output_message_after_search_process(new_res, m.chat.id, m)
        flags.location = False

    else:
        bot.send_message(m.chat.id, text="I do not understand you")


bot.polling(none_stop=True, interval=0)
