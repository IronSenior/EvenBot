#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import private as tk
from Funciones.teclado import *
from Funciones import formato
import time
from event import Event
from DataBase import *


# CONFIGURACION DE TELEGRAM
token = tk.tk()
bot = telebot.TeleBot(token)
initDataBase()

# Simplifica el enviar


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
    addTagToUser(cid, evento)

    msg = "Has agragado " + evento + " a tu lista"
    bot.send_message(cid, msg)


@bot.message_handler(commands=['NewEvent'])
def new_event(m):
    cid = m.chat.id
    bot.send_message(cid, "¿Qué tipo de eventos vas a organizar?",
                     reply_markup=keyboard_ntags)


@bot.callback_query_handler(func=lambda eve: eve.data in ['n_tech', 'n_music', 'n_sport', 'n_art', 'n_otros'])
def get_tag(eve):
    evento = eve.data[2:]
    cid = eve.message.chat.id
    # Guardar en base de datos lo que ha elegido
    # Notificar a los usuarios del tag el nuevo evento

    msg = "Has seleccionado " + evento + " como tipo de evento"
    send(eve.message, msg)
    time.sleep(1)
    send(eve.message, "¿Cuando va a ser tu evento? (M/D/Y-H:M)")
    bot.register_next_step_handler(eve.message, get_fecha)


def get_fecha(m):
    cid = m.chat.id
    if formato.es_fecha(m.text):
        fecha = m.text.split("-")[0]
        hora = m.text.split("-")[1]
        # Guardar fecha
        send(m, "¿Dónde va a ser tu evento? Enviame la ubicación")
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
        get_lugar2(m)


def get_lugar2(m):
    cid = m.chat.id
    bot.send_message(cid, "¿Quieres probar otra vez?",
                     reply_markup=keyboard_lugar)


@bot.callback_query_handler(func=lambda lugar: lugar.data in ["I", "O"])
def get_lugar3(lugar):
    if lugar.data == "I":
        send(m, "¿Dónde va a ser tu evento? Enviame la ubicación (Desde el móvil)")
        bot.register_next_step_handler(lugar.message, get_lugar)
    else:
        get_group(lugar.message)


def get_group(m):
    cid = m.chat.id
    bot.send_message(
        cid, "¿Tienes un grupo de telegram del evento?", reply_markup=keyboard_group)


@bot.callback_query_handler(func=lambda group: group.data in ['S', 'N'])
def get_group2(group):
    if group.data == "S":
        send(group.message, "Enviame el link de invitación del grupo")
        bot.register_next_step_handler(group.message, get_group3)
    else:
        send(group.message, "¿Cómo se llama tu evento?")
        bot.register_next_step_handler(group.message, get_name)


def get_group3(m):
    link = m.text
    if es_link(link):
        send(m, "¿Cómo se llama tu evento?")
        bot.register_next_step_handler(m, get_name)
    else:
        send(m, "No has mandado el link correctamente, prueba otra vez")
        bot.register_for_reply(m, get_group3)


def get_name(m):
    name = m.text
    send(m, "Por último, enviame una pequeña descripción de tu evento")
    bot.register_next_step_handler(m, get_desc)


def get_desc(m):
    desc = m.text
    send(m, "Tu evento ha sido guardado correctamente")


def sendEventMessage(m, event):
    sendMarkdownMessage(m, """
        🎟 *EVENTO* 🎟

        *Tipo: * {}
        *Nombre: * {}
        *Fecha: * {}
        *Descripción: * {}
        *URL del grupo: * {}
    """.format(event.tag, event.name, event.date, event.description, event.group))
    if not event.locX == 0 and not event.locY == 0:
        sendLocation(m, event.locX, event.locY)


@bot.message_handler(commands=['viewEvents'])
def view_events(m):
    cid = m.chat.id

    tag = getTagOfUser(cid)
    receivedEvents = getDataByTag(tag)

    events = list(map(lambda eventArray: Event(
        eventArray[0], eventArray[1], eventArray[2], eventArray[3], eventArray[4], eventArray[5], eventArray[6], eventArray[7]), receivedEvents))

    for event in events:
        sendEventMessage(m, event)


bot.polling()
