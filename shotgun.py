import time

inputType = None
inputID = None

"""Funciones"""
def typeVerification(typeToVerify):
	global inputType 
	if typeToVerify == 'asset':
		inputType = 'Asset'
		return True
	elif typeToVerify == 'shot':
		inputType = 'Shot'
		return True
	else:
		return False
def idVerification(idToVerify):
	try:
		idToVerify = int(idToVerify)
	except:
		return False


"""Analizar respuesta: Asset o Shot"""
while not typeVerification(raw_input("Elige una de las opciones:\n-Asset\n-Shot\n").lower()):
	print "\n---Tipo de dato invalido. Vuelva a intentarlo---\n"
"""Analizar el ID"""
while not idVerification(raw_input("Ahora introduzca el ID del %s:\n" %inputType)):
	print "\n---Tipo de dato invalido o inexistente. Vuelva a intentarlo---\n"
print "Correct ID"
time.sleep(5)
