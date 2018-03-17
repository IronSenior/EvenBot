#!/usr/bin/env python
#-*- coding:utf-8 -*-

from telebot import *

keyboard_tags = types.InlineKeyboardMarkup()

keyboard_tags.add(types.InlineKeyboardButton("Tech",callback_data="tech"),
                 types.InlineKeyboardButton("Music",callback_data="music"),
                 types.InlineKeyboardButton("Sport",callback_data="sport"),
                 types.InlineKeyboardButton("Art",callback_data="art"), 
                 types.InlineKeyboardButton("Otros",callback_data="otros")
                 )
