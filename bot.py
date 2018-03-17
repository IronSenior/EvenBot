#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import private as tk
from Funciones.teclado import *
from event import Event

# CONFIGURACION DE TELEGRAM
token = tk.tk()
bot = telebot.TeleBot(token)

# Simplifica el enviar


def send(m, message_text):
    bot.send_message(m.chat.id, message_text)


def sendMarkdownMessage(m, message_text):
    bot.send_message(m.chat.id, message_text, parse_mode="Markdown")


def sendLocation(m, lat, long):
    bot.send_location(m.chat.id, lat, long)


@bot.message_handler(commands=['start'])
def start(m):
    cid = m.chat.id
    send(m, "Hola")
    bot.send_message(cid, "¿Qué tipo de eventos te gustaría ver?",
                     reply_markup=keyboard_tags)


@bot.callback_query_handler(func=lambda eve: eve.data in ['tech', 'music', 'sport', 'art', 'otros'])
def calback_handler(eve):
    evento = eve.data
    cid = eve.message.chat.id
    # Guardar en base de datos lo que ha elegido

    msg = "Has agragado " + evento + " a tu lista"
    bot.send_message(cid, msg)


@bot.message_handler(commands=['NewEvent'])
def new_event(m):
    cid = m.chat.id
    bot.send_message(cid, "¿Qué tipo de eventos vas a organizar?",
                     reply_markup=keyboard_ntags)


@bot.callback_query_handler(func=lambda eve: eve.data in ['n_tech', 'n_music', 'n_sport', 'n_art', 'n_otros'])
def calback_handler2(eve):
    evento = eve.data[2:]
    cid = eve.message.chat.id
    # Guardar en base de datos lo que ha elegido
    # Notificar a los usuarios del tag el nuevo evento
    msg = "Has seleccionado " + evento + " como tu tipo de evento"
    bot.send_message(cid, msg)


def sendEventMessage(m, event):
    sendMarkdownMessage(m, """
        🎟 *EVENTO* 🎟

        *Tipo: * {}
        *Nombre: * {}
        *Fecha: * {}
        *Descripción: * {}
        *URL del grupo: * {}
    """.format(event.tag, event.name, event.date, event.description, event.group))
    sendLocation(m, event.locX, event.locY)


@bot.message_handler(commands=['viewEvents'])
def view_events(m):
    cid = m.chat.id
    # Obtener el tag del usuario de la base de datos
    tag = 'tech'  # Dummy Tag
    # Obtener de base de datos los eventos correspondientes a ese tag
    dummyEvents = [['17/03/2018', 'tech', 'Hackathon1', 'http://google.es',
                    37.864741, -4.795475, 'Best description 1', 'Image1.png'],
                   ['17/03/2018', 'tech', 'Hackathon2', 'http://google.es',
                    37.864741, -4.795475, 'Best description 2', 'Image2.png']]

    events = list(map(lambda eventArray: Event(
        eventArray[0], eventArray[1], eventArray[2], eventArray[3], eventArray[4], eventArray[5], eventArray[6], eventArray[7]), dummyEvents))

    for event in events:
        sendEventMessage(m, event)


bot.polling()
