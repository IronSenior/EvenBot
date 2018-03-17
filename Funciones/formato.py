def es_fecha(texto):
	try:
		msg = texto.split(" ")
		fecha = msg[0]
		hora = msg[1]

		if (fecha[4] == "-") and (fecha[7] == "-") and (hora[2] == ":"):
			return True

	except:
		return False

def es_link(link):
	print link[:1]
	if link[:2] == "t.":
		return True


es_link("t.dasd")