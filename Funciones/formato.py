def es_fecha(texto):
	try:
		msg = texto.split("-")
		fecha = msg[0]
		hora = msg[1]

		if (fecha[2] == "/") and (fecha[5] == "/") and (hora[2] == ":"):
			return True

	except:
		return False