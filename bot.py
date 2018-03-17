#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import private as tk
from Funciones.teclado import *
from Funciones import formato
import time

#CONFIGURACION DE TELEGRAM
token = tk.tk()
bot = telebot.TeleBot(token)

#Simplifica el enviar
def send(m, message_text):
    bot.send_message(m.chat.id, message_text)

userStep = {}

def get_user_step(cid):
	if cid in userStep:
		return userStep[cid]
	else:
		userStep[cid] = 0
		print "New user detected, who hasn't used \"/start\" yet"
		return 0

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
def get_tag(eve):
	evento = eve.data[2:]
	cid = eve.message.chat.id
	#Guardar en base de datos lo que ha elegido

	msg = "Has seleccionado " + evento + " como tipo de evento"
	send(eve.message, msg)
	send(eve.message, "¿Cuando va a ser tu evento?")
	bot.register_next_step_handler(eve.message, get_fecha)

def get_fecha(m):
	cid = m.chat.id
	if formato.es_fecha(m.text):
		fecha = m.text
		#Guardar fecha
		send(m, "¿Dónde va a ser tu evento? Envianos la ubicación")
		bot.register_next_step_handler(m, get_lugar)
	else:
		send(m, "Error con el formato de la fecha y la hora, (M/D/Y-H:M)")
		send(m, "¿Cuando va a ser tu evento?")
		bot.register_next_step_handler(m, get_fecha)


def get_lugar(m):
	cid = m.chat.id
	if m.location:
		x = m.location['latitude']
		y = m.latitude['longitude']
	else:
		send(m, "Error, debes mandar una ubicación")
		bot.register_next_step_handler(m, get_lugar)








bot.polling()

