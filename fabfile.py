import re
from fabric.api import run, env, local, get, settings, execute
from fabric.decorators import hosts, runs_once
from datetime import datetime
from utilities import send_alert, abrir_log, cerrar_log


archivo_de_ips = open('IPs', 'r')
archivo_de_credenciales = open('credenciales', 'r')
lista_de_ips = []
lista_de_hostnames = []
traductor = {}
mgmt_ip = '172.18.0.33'
carpeta_de_backups = '/config-backups/'
subcarpeta_de_fws = 'FWs/'
carpeta_de_logs = '/logs-backups/'
archivo_de_logs = carpeta_de_logs  + 'pretty_log.log'
archivo_de_logs_crudos = carpeta_de_logs  + 'log.log'

# Armo un string con la hora de la corrida
ahora = datetime.now()
if ahora.month < 10:
	mes = '0' + str(ahora.month)
else:
	mes = str(ahora.month)

if ahora.day < 10:
	dia = '0' + str(ahora.day)
else:
	dia = str(ahora.day)

if ahora.hour < 10:
	hora = '0' + str(ahora.hour)
else:
	hora = str(ahora.hour)

if ahora.minute < 10:
	minutos = '0' + str(ahora.minute)
else:
	minutos = str(ahora.minute)

if ahora.second < 10:
	segundos = '0' + str(ahora.second)
else:
	segundos = str(ahora.second)

ahora_string = str(ahora.year) + '_' + mes + '_' + dia + '-' + hora + '_' + minutos + '_' + segundos


# Recorro el archivo de IPs linea por linea eliminando los enters y generando un array con las IPs
for linea in archivo_de_ips.readlines():
	try:
		parsed_line = re.search('^\s*(\d+\.\d+.\d+\.\d+)\,\s*([^s\n,]+)\,\s*(cisco|vyos|osv|sbc)',linea)
		lista_de_ips.append(parsed_line.group(1))
		hostname = parsed_line.group(2)
		os = parsed_line.group(3)
		traductor.update({lista_de_ips[len(lista_de_ips)-1]: (hostname, os)})
	except:
		pass

print(traductor)

# En este punto lista_de_ips es un array que contiene las IPs de los dispositivos a respaldar
# Seteo la variable de ambiente con los hosts a respaldar
env.hosts = lista_de_ips

# Recorro el archivo de credenciales linea por linea eliminando comentarios y buscando user: y pass:
for linea in archivo_de_credenciales.readlines():
	try:
		comentario = re.search('^(\s*)(#)',linea).group(2)
	except:
		try:
			usuario = re.search('(user:)([^\s^\n]+)',linea).group(2)
		except:
			pass
		try:
			password = re.search('(pass:)([^\s^\n]+)',linea).group(2)
		except:
			pass

# En este punto las variables usuario y password contienen las credenciales
# Seteo las variables de entorno para usuario y password
env.user = usuario
env.password = password
# Seteo el timeout de los comandos remotos en 15 segundos
env.command_timeout = 10

# Cierro los archivos que abri
try:
	archivo_de_ips.close()
	print('Archivo de IPs cerrado')
except:
	print('No se pudo cerrar el archivo de IPs')

try:
	archivo_de_credenciales.close()
	print('Archivo de credenciales cerrado')
except:
	print('No se pudo cerrar el archivo de credenciales')


@runs_once
@hosts('localhost')
def comenzar():
	abrir_log()

@runs_once
@hosts('localhost')
def terminar():
	cerrar_log()

def start():
	execute(comenzar)
def stop():
	execute(terminar)

# Funcion que copia por scp las configuraciones de los equipos
def respaldar_vyos():
	# Abro los archivos de log para loggear el resultado
	pretty_log = open(archivo_de_logs, 'a')
	raw_log = open(archivo_de_logs_crudos, 'a')

	print('CORRIENDO RESPALDAR_VYOS')
	raw_log.write('CORRIENDO RESPALDAR_VYOS')

	print('Respaldando ' + traductor[env.host_string][0])
	raw_log.write('Respaldando: ' + traductor[env.host_string][0])

	try:
		with settings(warn_only=True):
			filename = 'config_' + traductor[env.host_string][0] + '_' + ahora_string + '.cfg'
			resultado1 = run('/bin/bash -c -i "show configuration commands | no-more"', shell=False, shell_escape=True, warn_only=True)
			raw_log.write(resultado1)
		if resultado1.failed:			
			send_alert(traductor[env.host_string][0])
			err_msg = 'ATENCION!!!! ' + traductor[env.host_string][0] + ' Failed!\n'
			print(err_msg)
			pretty_log.write(err_msg)
			pretty_log.close()
			raw_log.write(err_msg)
		else:
			temp_result = open(carpeta_de_backups + subcarpeta_de_fws + filename, 'w')
			temp_result.write(resultado1.stdout)
			temp_result.close() 
			success_msg = traductor[env.host_string][0] + ' Succeed!\n'
			print(success_msg)
			pretty_log.write(success_msg)
			pretty_log.close()
			raw_log.write(success_msg)
	except:
		try:
			send_alert(traductor[env.host_string][0])
			err_msg = 'ATENCION!!!! ' + traductor[env.host_string][0] + ' Failed!\n'
			print(err_msg)
			pretty_log.write(err_msg)
			pretty_log.close()
			raw_log.write(err_msg)
		except:
			err_msg = 'ATENCION!!!! ' + traductor[env.host_string][0] + ' Failed!\n'
			err_msg += 'No se pudo enviar mail!\n'
			print(err_msg)
			pretty_log.write(err_msg)
			pretty_log.close()
			raw_log.write(err_msg)
	raw_log.close()


def respaldar_cisco():
	# Abro el archivo de logs para loggear el resultado
	pretty_log = open(archivo_de_logs, 'a')
	raw_log = open(archivo_de_logs_crudos, 'a')

	print('CORRIENDO RESPALDAR_CISCO')
	raw_log.write('CORRIENDO RESPALDAR_CISCO')

	filename = 'config_' + traductor[env.host_string][0] + '_' + ahora_string + '.cfg'
	raw_log.write('Respaldando: ' + traductor[env.host_string][0])

	diccionario_de_prompts = {
		'Address or name of remote host []? ': mgmt_ip,
		'Destination filename [fw-clientes-1-confg]? ': subcarpeta_de_fws + filename,
		'Destination filename [fw-clientes-2-confg]? ': subcarpeta_de_fws + filename,
	}

	try:
		with settings(prompts=diccionario_de_prompts, warn_only=True):
			resultado = run('copy startup-config tftp:', shell=False, shell_escape=True)
			raw_log.write(resultado)
		if resultado.failed:
			err_msg = 'ATENCION!!!! ' + traductor[env.host_string][0] + ' Failed!\n'
			try:
				send_alert(traductor[env.host_string][0])
			except:
				err_msg += 'No se pudo enviar el mail!\n'
			print(err_msg)
			pretty_log.write(err_msg)
			pretty_log.close()
			raw_log.write(err_msg)
		else:
			try:
				# En el caso de que la terminal remota no envie los errores a stderr, los busco manualmente
				re.search('(error)', resultado.stdout, re.IGNORECASE).groups()
				err_msg = 'ATENCION!!!! ' + traductor[env.host_string][0] + ' Failed!\n'
				try:
					send_alert(traductor[env.host_string][0])
				except:
					err_msg += 'No se pudo enviar el mail!\n'
				print(err_msg)
				pretty_log.write(err_msg)
				pretty_log.close()
				raw_log.write(err_msg)
			except:
				success_msg = traductor[env.host_string][0] + ' Succeed!\n'
				print(success_msg)
				pretty_log.write(success_msg)
				pretty_log.close()
				raw_log.write(success_msg)
	except:			
			err_msg = 'ATENCION!!!! ' + traductor[env.host_string][0] + ' Failed!\n'
			try:
				send_alert(traductor[env.host_string][0])
			except:
				err_msg += 'No se pudo enviar el mail!\n'
			print(err_msg)
			pretty_log.write(err_msg)
			pretty_log.close()
			raw_log.write(err_msg)
	raw_log.close()

# Funcion que respalda el osv completo.
def respaldar_osv():
	print('CORRIENDO RESPALDAR_OSV')
	print('Respaldando ' + traductor[env.host_string][0])
	# Abro el archivo de log para loggear el resultado
	pretty_log = open(archivo_de_logs, 'a')
	
	# Me conecto y le pido a la OSV que haga el respaldo
	diccionario_de_prompts = {
		'Address or name of remote host []? ': mgmt_ip,
		'Destination filename [fw-clientes-1-confg]? ': filename,
		'Destination filename [fw-clientes-2-confg]? ': filename,
	}

	with settings(prompts=diccionario_de_prompts, warn_only=True):
		resultado = run('export8k -local', shell=False, shell_escape=True)



def respaldar_configuraciones():
	if traductor[env.host_string][1] == 'cisco':
		respaldar_cisco()
	elif traductor[env.host_string][1] == 'vyos':
		respaldar_vyos()
	elif traductor[env.host_string][1] == 'osv':
		respaldar_osv()
	elif traductor[env.host_string][1] == 'sbc':
		respaldar_sbc()
	else:
		pass


# Funcion que se conecta a los equipos y respalda las configuraciones en el servidor tftp
#def respaldar_configuraciones():
#	run('/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper begin', shell=False, shell_escape=True)
#	run('/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper save tftp://' + mgmt_ip + '/$(date +%Y%m%d-%H%M%S)_$(hostname).cfg', shell=False, shell_escape=True, timeout=5, warn_only=True)


#save tftp://172.18.0.33/$(date +%Y%m%d-%H%M%S)_$(hostname).cfg
#bash -c "python -c 'from utilities import abrir_log; abrir_log()'; fab respaldar_configuraciones; python -c'from utilities import cerrar_log; cerrar_log()'"