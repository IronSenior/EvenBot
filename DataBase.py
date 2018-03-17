#!./venv/bin/python

import sqlite3


def initDataBase():
    conn = sqlite3.connect('events.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS 'EVENT' (
             ID          INTEGER    PRIMARY KEY AUTOINCREMENT,
             FECHA       TEXT       NOT NULL,
			 TAG         CHAR(10),
	         NOMBRE      CHAR(50)   NOT NULL,
	         GROUP_      CHAR(20),
	         X           REAL       NOT NULL,
	         Y           REAL       NOT NULL,
	         DESCIPCION  TEXT,
	         CHAT_ID     INT        NOT NULL
    );''')

    conn.execute('''CREATE TABLE IF NOT EXISTS 'TAGCHAT'
            (CHAT_ID     TEXT       PRIMARY KEY,
            TAG         CHAR(10)   NOT NULL
    );''')

    conn.close()


def newData(fecha, tag, nombre, grupo, x, y, descipcion, cid):

    conn = sqlite3.connect('events.db')
    cur = conn.cursor()
    # print ("%s, %s, %s ,%i, %i, %s, %s" % (tag,nombre,grupo,x,y,descipcion,imagen));

    # fecha,
    cur.execute("INSERT INTO EVENT VALUES (null, '{dt}', '{tg}', '{nom}', '{gr}', {x_}, {y_}, '{desc}', '{im}');".
                format(dt=fecha, tg=tag, nom=nombre, gr=grupo, x_=x, y_=y, desc=descipcion, im=cid))

    eventId = cur.lastrowid

    conn.commit()
    conn.close()

    return eventId

def getDatabyID(event_id):
    conn = sqlite3.connect('events.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM {table} WHERE ID='{id}'".
                format(table="event", id=event_id))
    data = cur.fetchall()

    conn.close()

    return data[0]

def getData():

    conn = sqlite3.connect('events.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM {tn}".
                format(tn="event"))
    data = cur.fetchall()

    conn.close()

    return data


def getDataByTag(tag):

    conn = sqlite3.connect('events.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM {table} WHERE TAG='{tg}'".
                format(table="event", tg=tag))
    data = cur.fetchall()

    conn.close()

    return data


def getUsersWithTag(tag):

    conn = sqlite3.connect('events.db')
    cur = conn.cursor()

    cur.execute("SELECT chat_id FROM {table} WHERE TAG='{tg}'".
                format(table="tagchat", tg=tag))
    data = cur.fetchall()

    conn.close()
    print data
    return data


def getTagOfUser(chatId):
    conn = sqlite3.connect('events.db')
    cur = conn.cursor()

    cur.execute("SELECT tag FROM {table} WHERE CHAT_ID='{chatid}'".
                format(table="tagchat", chatid=chatId))
    data = cur.fetchall()

    conn.close()

    return data[0][0]


def addTagToUser(chatId, tag):
    conn = sqlite3.connect('events.db')
    cur = conn.cursor()

    insert = "INSERT OR IGNORE INTO TAGCHAT VALUES ('{chatid}', '{tg}');".format(
        chatid=chatId, tg=tag)
    cur.execute(insert)

    update = "UPDATE TAGCHAT SET TAG = '{tg}' WHERE CHAT_ID = {chatid};".format(
        chatid=chatId, tg=tag)
    cur.execute(update)

    conn.commit()
    conn.close()

def deleteById(chatId):
    conn = sqlite3.connect('events.db')
    cur = conn.cursor()

    delete = "DELETE FROM {table} WHERE ID={chatId};".format(
        chatId=chatId, table="event")
    cur.execute(delete)

    conn.commit()
    conn.close()


initDataBase()
