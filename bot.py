#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import private as tk
from Funciones.teclado import *

#CONFIGURACION DE TELEGRAM
token = tk.tk()
bot = telebot.TeleBot(token)

#Simplifica el enviar
def send(m, message_text):
    bot.send_message(m.chat.id, message_text)


@bot.message_handler(commands=['start'])
def start(m):
	cid = m.chat.id
	send(m, "Hola")
	bot.send_message(cid,"¿Qué tipo de eventos te gustaría ver?",reply_markup=keyboard_tags)


@bot.callback_query_handler(func=lambda eve: eve.data in ['tech','music','sport','art', 'otros'])
def calback_handler(eve):
	evento = eve.data
	cid = eve.message.chat.id
	#Guardar en base de datos lo que ha elegido

	msg = "Has agragado " + evento + " a tu lista"
	bot.send_message(cid, msg)


@bot.message_handler(commands=['NewEvent'])
def new_event(m):
	cid = m.chat.id
	bot.send_message(cid,"¿Qué tipo de eventos vas a organizar?",reply_markup=keyboard_ntags)


@bot.callback_query_handler(func=lambda eve: eve.data in ['n_tech','n_music','n_sport','n_art','n_otros'])
def calback_handler2(eve):
	evento = eve.data[2:]
	cid = eve.message.chat.id
	#Guardar en base de datos lo que ha elegido

	msg = "Has seleccionado " + evento + " como tu tipo de evento"
	bot.send_message(cid, msg)



bot.polling()

