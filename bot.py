#!/mnt/data_1/code/python/EvenBot/venv/bin/python2.7
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


userData = {}


def sendMarkdownMessage(cid, message_text):
    bot.send_message(cid, message_text, parse_mode="Markdown")


def sendLocation(cid, lat, long):
    bot.send_location(cid, lat, long)


@bot.message_handler(commands=['start'])
def start(m):
    cid = m.chat.id
    send(m, "Hola")
    bot.send_message(cid, "¿Qué tipo de eventos te gustaría ver?",
                     reply_markup=keyboard_tags)


@bot.message_handler(commands=['stop'])
def stop(m):
    cid = m.chat.id
    if cid in userData:
        del userData[cid]
        send(m, "Se ha eliminado el evento")
    else:
        send(m, "No estas creando ningún evento")


@bot.message_handler(commands=["DlEvent"])
def dl_event(m):
    send(m, "Dime la id del evento que quieres eliminar")
    bot.register_next_step_handler(eve.message, get_dl)


def get_dl(m):
    if m.text.isdigit():
        try:
            # Eliminar evento por la id que se le ha pasado
            pass
        except:
            send(m, "Ha habido un error con la id que me has dado")
    else:
        send(m, "Debes decirme la id del evento que quieres borrar")


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
    send(m, "IMPORTANTE")
    send(m, "Si en algún momento te equivocas tendras que volver a empezar poniendo /NewEvent")
    send(m, "Si cambias de opinión utiliza /stop")
    bot.send_message(cid, "¿Qué tipo de eventos vas a organizar?",
                     reply_markup=keyboard_ntags)


@bot.callback_query_handler(func=lambda eve: eve.data in ['n_tech', 'n_music', 'n_sport', 'n_art', 'n_otros'])
def get_tag(eve):
    evento = eve.data[2:]
    cid = eve.message.chat.id
    userData[cid] = []
    userData[cid].append(evento)
    # Notificar a los usuarios del tag el nuevo evento

    msg = "Has seleccionado " + evento + " como tipo de evento"
    send(eve.message, msg)
    time.sleep(1)
    send(eve.message, "¿Cuando va a ser tu evento? Ej: 2018-06-26 16:45")
    bot.register_next_step_handler(eve.message, get_fecha)


def get_fecha(m):
    cid = m.chat.id
    if formato.es_fecha(m.text):
        userData[cid].append(m.text)
        send(m, "¿Dónde va a ser tu evento? Enviame la ubicación")
        bot.register_next_step_handler(m, get_lugar)
    else:
        send(m, "Error con el formato de la fecha y la hora, pogalo como en el ejemplo")
        send(m, "¿Cuando va a ser tu evento?")
        bot.register_next_step_handler(m, get_fecha)


def get_lugar(m):
    cid = m.chat.id
    if m.location:
        x = m.location.latitude
        y = m.location.longitude
        userData[cid].append(x)
        userData[cid].append(y)
        get_group(m)
    else:
        send(m, "Error, debes mandar una ubicación")
        get_lugar2(m)


def get_lugar2(m):
    cid = m.chat.id
    bot.send_message(cid, "¿Quieres probar otra vez?",
                     reply_markup=keyboard_lugar)


@bot.callback_query_handler(func=lambda lugar: lugar.data in ["I", "O"])
def get_lugar3(lugar):
    cid = lugar.message.chat.id
    if lugar.data == "I":
        send(lugar.message,
             "¿Dónde va a ser tu evento? Enviame la ubicación (Desde el móvil)")
        bot.register_next_step_handler(lugar.message, get_lugar)
    else:
        userData[cid].append("")
        userData[cid].append("")
        get_group(lugar.message)


def get_group(m):
    cid = m.chat.id
    bot.send_message(
        cid, "¿Tienes un grupo de telegram del evento?", reply_markup=keyboard_group)


@bot.callback_query_handler(func=lambda group: group.data in ['S', 'N'])
def get_group2(group):
    cid = group.message.chat.id
    if group.data == "S":
        send(group.message, "Enviame el link de invitación del grupo")
        bot.register_next_step_handler(group.message, get_group3)
    else:
        userData[cid].append("")
        send(group.message, "¿Cómo se llama tu evento?")
        bot.register_next_step_handler(group.message, get_name)


def get_group3(m):
    link = m.text
    cid = m.chat.id
    if formato.es_link(link):
        userData[cid].append(link)
        send(m, "¿Cómo se llama tu evento?")
        bot.register_next_step_handler(m, get_name)
    else:
        send(m, "No has mandado el link correctamente, prueba otra vez")
        bot.register_for_reply(m, get_group3)


def get_name(m):
    name = m.text
    cid = m.chat.id
    userData[cid].append(name)
    send(m, "Por último, enviame una pequeña descripción de tu evento")
    bot.register_next_step_handler(m, get_desc)


def get_desc(m):
    desc = m.text
    cid = m.chat.id
    userData[cid].append(desc)

    eventData = userData[cid]
    # Añadir imagen segun tag
    newEvent = Event(eventData[1], eventData[0], eventData[5], eventData[4],
                     eventData[2], eventData[3], eventData[6], 'temporal')

    eventId = newData(newEvent.date, newEvent.tag, newEvent.name, newEvent.group,
                      newEvent.locX, newEvent.locY, newEvent.description, newEvent.image)
    del userData[cid]
    send(m, "Tu evento ID " + str(eventId) + " ha sido guardado correctamente")

    chats = getUsersWithTag(newEvent.tag)
    inform_of_event(chats, newEvent)


def sendEventMessage(cid, event):
    sendMarkdownMessage(cid, """
        🎟 *EVENTO* 🎟

        *Tipo: * {}
        *Nombre: * {}
        *Fecha: * {}
        *Descripción: * {}
        *URL del grupo: * {}
    """.format(event.tag, event.name, event.date, event.description, event.group))
    if not event.locX == 0 and not event.locY == 0:
        sendLocation(cid, event.locX, event.locY)

def inform_of_event(chats, event):
    for chat in chats:
        sendEventMessage(chat, event)


@bot.message_handler(commands=['ViewEvents'])
def view_events(m):
    cid = m.chat.id

    tag = getTagOfUser(cid)
    receivedEvents = getDataByTag(tag)

    events = list(map(lambda eventArray: Event(
        eventArray[1], eventArray[2], eventArray[3], eventArray[4], eventArray[5], eventArray[6], eventArray[7], eventArray[8]), receivedEvents))

    for event in events:
        sendEventMessage(cid, event)


bot.polling()
