import os
import os.path
import time
from shotgun_api3 import Shotgun 

inputType = None
inputID = None
inputCode = None
requestVersions = None
requestVersionId = None

sg = Shotgun("https://upgdl.shotgunstudio.com", "NachoScript", "486c9aa2bf63e4a83f975e3928207342e15dfcfeb2066384d7e48f9da7087923" )

"""Funciones"""
def typeVerification(typeToVerify):
	global inputType 
	if typeToVerify == 'asset':
		inputType = 'Asset'
		os.system('CLS')
		return True
	elif typeToVerify == 'shot':
		inputType = 'Shot'
		os.system('CLS')
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
		os.system('CLS')
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
def assignNewName():
	global requestVersions, inputCode
	newNameOption = raw_input("Desea crear un nuevo nombre? (s/n)\n")
	if newNameOption == 'n':
		inputCode = requestVersions[len(requestVersions)-1]['code']
		inputCode = "%s%03d" %(inputCode[:len(inputCode)-3], int(inputCode[len(inputCode)-3:])+1)
		print inputCode
	else:
		possibleCode = raw_input("Escriba el nombre a asignar\n")
		inputCode = "%s v001" %possibleCode
		for version in requestVersions:
			if possibleCode.lower() in version["code"].lower():
				inputCode = "%s%03d" %(version["code"][:len(version["code"])-3], int(version["code"][len(version["code"])-3:])+1)
	confirmCode = raw_input("El nombre de la nueva version sera:\n%s\nEsta de acuerdo? (s/n)" %inputCode)
	if confirmCode.lower() == 'n':
		return False
	else:
		os.system('CLS')
		return True
def createNewVersion():
	global inputCode, inputID, inputType, requestVersionId
	description = raw_input("Escribe una descripcion de tu version:\n")
	data = {
		'code': inputCode,
		'entity': {'id': inputID, 'type':inputType},
		'description': description,
		'sg_task': {'id': 2252 , 'type':'Task'},
		'user': {'id':84, 'type': 'HumanUser'},
		'sg_status_list': 'rev',
		'project': {'id':110, 'type':'Project'}
	}
	result = sg.create("Version", data)
	requestVersionId = result['id']
	print "Version created!\n"

def addValidMedia():
	global requestVersionId
	file_path = raw_input("Introduzca la ruta al archivo media a subir (incluya la extension):\n")
	if os.path.isfile(file_path) :
		sg.upload("Version", requestVersionId, file_path, field_name="sg_uploaded_movie", display_name="Media")
		return True
	else:
		return False

"""Analizar respuesta: Asset o Shot"""
while not typeVerification(raw_input("Elige una de las opciones:\n-Asset\n-Shot\n").lower()):
	print "\n---Tipo de dato invalido. Vuelva a intentarlo---\n"
"""Analizar el ID"""
while not idVerification(raw_input("Ahora introduzca el ID del %s:\n" %inputType)):
	print "\n---Tipo de dato invalido o inexistente. Vuelva a intentarlo---\n"
"""Creacion de un nombre"""
findVersions()
while not assignNewName():
	print ''
"""POST request"""
createNewVersion()
while not addValidMedia():
	print ''
print "Todo listo\nGracias por usar esta herramienta!"
time.sleep(5)
