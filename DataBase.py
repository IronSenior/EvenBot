#!./venv/bin/python

import sqlite3

def initDataBase():
	conn = sqlite3.connect('events.db')
	conn.execute('''CREATE TABLE EVENT
			(FECHA       TEXT       NOT NULL,
			 TAG         CHAR(10),
	         NOMBRE      CHAR(50)   NOT NULL,
	         GROUP_      CHAR(20),
	         X           REAL       NOT NULL,
	         Y           REAL       NOT NULL,
	         DESCIPCION  TEXT,
	         IMAGEN      CHAR(100)  NOT NULL);''')

	conn.close()



def newData(fecha,tag,nombre,grupo,x,y,descipcion,imagen):

	conn = sqlite3.connect('events.db')
	cur = conn.cursor()
	# print ("%s, %s, %s ,%i, %i, %s, %s" % (tag,nombre,grupo,x,y,descipcion,imagen));

	# fecha,
	cur.execute ("INSERT INTO EVENT VALUES ('{dt}', '{tg}', '{nom}', '{gr}', {x_}, {y_}, '{desc}', '{im}');".\
	format(dt=fecha, tg=tag, nom=nombre, gr=grupo, x_=x, y_=y, desc=descipcion, im=imagen));

	conn.commit()
	conn.close()

def getData():

	conn = sqlite3.connect('events.db')
	cur = conn.cursor()

	cur.execute("SELECT * FROM {tn}".\
		format(tn="event"));
	print (cur.fetchall())

	conn.close()

def getDataByTag(tag):

	conn = sqlite3.connect('events.db')
	cur = conn.cursor()

	cur.execute("SELECT * FROM {table} WHERE TAG='{tg}'".\
		format(table="event", tg=tag));
	print (cur.fetchall())

	conn.close()

initDataBase()
newData("fecha","tag","nombre","grupo",1,1,"descipcion","imagen")
getData()
