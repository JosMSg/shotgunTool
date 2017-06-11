import time
from shotgun_api3 import Shotgun 

inputType = None
inputID = None
requestVersions = None

sg = Shotgun("https://upgdl.shotgunstudio.com",
                          login="ignacho",
                          password="Minions2793")

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
	global inputType
	global inputID
	try:
		idToVerify = int(idToVerify)
	except:
		return False
	request = sg.find_one(inputType, [["id", "is", idToVerify]], ["id", "code"]) 
	if request != None:
		inputID = idToVerify
		print "El Id %s pertenece al %s %s" %(inputID, inputType, request['code'])
		return True
	else: 
		return False
def findVersions():
	global inputType, inputID, requestVersions
	filters = [['entity','is', {'id': inputID, 'type': inputType}]]
	fields = ['id', 'code']
	requestVersions= sg.find("Version", filters, fields)
	print "Versiones creadas en el %s seleccionado:\n" %inputType
	for version in requestVersions:
		print version['code']

"""Analizar respuesta: Asset o Shot"""
while not typeVerification(raw_input("Elige una de las opciones:\n-Asset\n-Shot\n").lower()):
	print "\n---Tipo de dato invalido. Vuelva a intentarlo---\n"
"""Analizar el ID"""
while not idVerification(raw_input("Ahora introduzca el ID del %s:\n" %inputType)):
	print "\n---Tipo de dato invalido o inexistente. Vuelva a intentarlo---\n"
findVersions()

time.sleep(5)
