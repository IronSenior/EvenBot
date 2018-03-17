#!./venv/bin/python

import sqlite3

def init():
	conn = sqlite3.connect('events.db')
	# print ("Opened database successfully");
	# FECHA       DATE       NOT NULL,
	conn.execute('''CREATE TABLE EVENT
			(
			TAG         CHAR(10),
	         NOMBRE      CHAR(50)   NOT NULL,
	         GROUP_       CHAR(20),
	         X           REAL       NOT NULL,
	         Y           REAL       NOT NULL,
	         DESCIPCION  TEXT,
	         IMAGEN      CHAR(100)  NOT NULL);''')

	# print ("Table created successfully");
	conn.close()



def new_data(tag,nombre,grupo,x,y,descipcion,imagen):

	conn = sqlite3.connect('events.db')
	cur = conn.cursor()
	# print ("Opened database successfully");
	print ("%s, %s, %s ,%i, %i, %s, %s" % (tag,nombre,grupo,x,y,descipcion,imagen));

	# fecha,
	cur.execute ("INSERT INTO EVENT VALUES ('{tg}', '{nom}', '{gr}', {x_}, {y_}, '{desc}', '{im}');".\
	format(tg=tag, nom=nombre, gr=grupo, x_=x, y_=y, desc=descipcion, im=imagen));

	# print ("Table created successfully");
	conn.commit()
	conn.close()



def get_data():

	conn = sqlite3.connect('events.db')
	cur = conn.cursor()
	print ("Opened database successfully");

	cur.execute("SELECT * FROM {tn}".\
		format(tn="event"));
	print (cur.fetchall())

	print ("Table created successfully");
	conn.close()



init()
new_data("tag","name","group",1,1,"descipcion","imagen")
