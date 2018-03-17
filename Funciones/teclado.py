#!/mnt/data_1/code/python/EvenBot/venv/bin/python2.7
#-*- coding:utf-8 -*-

from telebot import *

keyboard_tags = types.InlineKeyboardMarkup()

keyboard_tags.add(types.InlineKeyboardButton("Tech",callback_data="tech"),
                 types.InlineKeyboardButton("Music",callback_data="music"),
                 types.InlineKeyboardButton("Sport",callback_data="sport"),
                 types.InlineKeyboardButton("Art",callback_data="art"),
                 types.InlineKeyboardButton("Otros",callback_data="otros")
                 )

keyboard_ntags = types.InlineKeyboardMarkup()

keyboard_ntags.add(types.InlineKeyboardButton("Tech",callback_data="n_tech"),
                 types.InlineKeyboardButton("Music",callback_data="n_music"),
                 types.InlineKeyboardButton("Sport",callback_data="n_sport"),
                 types.InlineKeyboardButton("Art",callback_data="n_art"),
                 types.InlineKeyboardButton("Otros",callback_data="n_otros")
                 )

keyboard_lugar = types.InlineKeyboardMarkup()

keyboard_lugar.add(types.InlineKeyboardButton("Si",callback_data="I"),
                  types.InlineKeyboardButton("No", callback_data="O"))

keyboard_group = types.InlineKeyboardMarkup()

keyboard_group.add(types.InlineKeyboardButton("Si",callback_data="S"),
                  types.InlineKeyboardButton("No", callback_data="N"))
