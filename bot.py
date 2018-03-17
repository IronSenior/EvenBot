#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import private as tk

#CONFIGURACION DE TELEGRAM
token = tk.tk()
bot = telebot.Telebot(token)

#Simplifica el enviar
def send(m, message_text):
    bot.send_message(m.chat.id, message_text)