import re
import os
from fabric.api import run, env, local, get, settings, execute
from fabric.decorators import hosts, runs_once
from datetime import datetime
from utilities import send_alert, abrir_log, cerrar_log, send_mail

archivo_de_ips = open('IPs', 'r')
archivo_de_credenciales = open('credenciales', 'r')
lista_de_ips = []
lista_de_hostnames = []
traductor = {}
mgmt_ip = '172.18.0.33'
carpeta_de_backups = '/config-backups/'
subcarpeta_de_fws = 'FWs/'
subcarpeta_de_sbcs = 'SBCs/'
subcarpeta_de_osvs = 'OSVs/'
carpeta_de_logs = '/logs-backups/'
archivo_de_logs = carpeta_de_logs + 'pretty_log.log'
archivo_de_logs_crudos = carpeta_de_logs + 'log.log'
usuario_osv = 'root'
password_osv = 'T@R63dis'
usuario_sbc = 'administrator'
password_sbc = 'Asd123!.'
sbc_backup_path = '/opt/siemens/openbranch/var/mngmt/xml/v9.2/*.xml'
# Armo un string con la hora de la corrida
ahora_string = datetime.now().strftime('%Y-%m-%d__%H-%M-%S')

# Recorro el archivo de IPs linea por linea eliminando los enters y generando un array con las IPs
for linea in archivo_de_ips.readlines():
    try:
        parsed_line = re.search('^\s*(\d+\.\d+.\d+\.\d+),\s*([^\s\n,]+),\s*(cisco|vyos|osv|sbc)', linea)
        lista_de_ips.append(parsed_line.group(1))
        hostname = parsed_line.group(2)
        sis_op = parsed_line.group(3)
        traductor.update({lista_de_ips[len(lista_de_ips) - 1]: (hostname, sis_op)})
    except:
        pass

print(traductor)

# En este punto lista_de_ips es un array que contiene las IPs de los dispositivos a respaldar
# Seteo la variable de ambiente con los hosts a respaldar
env.hosts = lista_de_ips

# Recorro el archivo de credenciales linea por linea eliminando comentarios y buscando user: y pass:
for linea in archivo_de_credenciales.readlines():
    try:
        comentario = re.search('^(\s*)(#)', linea).group(2)
    except:
        try:
            usuario = re.search('(user:)([^\s^\n]+)', linea).group(2)
        except:
            pass
        try:
            password = re.search('(pass:)([^\s^\n]+)', linea).group(2)
        except:
            pass

# En este punto las variables usuario y password contienen las credenciales
# Seteo las variables de entorno para usuario y password
env.user = usuario
env.password = password
# Seteo el timeout de los comandos remotos en 10 segundos
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
    raw_log.write('CORRIENDO RESPALDAR_VYOS\n')

    print('Respaldando ' + traductor[env.host_string][0])
    raw_log.write('Respaldando: ' + traductor[env.host_string][0] + '\n')

    try:
        with settings(warn_only=True):
            filename = 'config_' + traductor[env.host_string][0] + '_' + ahora_string + '.cfg'
            resultado1 = run('/bin/bash -c -i "show configuration commands | no-more"', shell=False, shell_escape=True,
                             warn_only=True)
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
    raw_log.write('CORRIENDO RESPALDAR_CISCO\n')

    filename = 'config_' + traductor[env.host_string][0] + '_' + ahora_string + '.cfg'
    raw_log.write('Respaldando: ' + traductor[env.host_string][0] + '\n')


    try:
        # Consigo el hostname del dispositivo
        with settings(warn_only=True):
            resultado = run('show running | inc hostname', shell=False, shell_escape=True)
            nombre_de_host = re.search('^hostname ([\w,-]+)', resultado).group(1).lower()
            print('EL NOMBRE DEL HOST ES:', nombre_de_host)
            diccionario_de_prompts = {
                'Address or name of remote host []? ': mgmt_ip,
                'Destination filename [' + nombre_de_host + '-confg]? ': subcarpeta_de_fws + filename,
            }

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
    # Abro el archivo de logs para loggear el resultado
    pretty_log = open(archivo_de_logs, 'a')
    raw_log = open(archivo_de_logs_crudos, 'a')

    print('CORRIENDO RESPALDAR_SBC ')
    raw_log.write('CORRIENDO RESPALDAR_SBC ')
    print('Respaldando: ' + traductor[env.host_string][0])
    raw_log.write('Respaldando: ' + traductor[env.host_string][0])

    try:
        with settings(user=usuario_osv, password=password_osv, warn_only=True, command_timeout=600):
            resultado = run('export8k -local')
            raw_log.write(resultado)
        with settings(user=usuario_osv, password=password_osv, warn_only=True, command_timeout=300):
            resultado2 = get('/software/toolkit/*', carpeta_de_backups + subcarpeta_de_osvs)
        if resultado.failed or not resultado2.succeeded:
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


# Funcion que respalda el sbc.
def respaldar_sbc():
    # Abro el archivo de logs para loggear el resultado
    pretty_log = open(archivo_de_logs, 'a')
    raw_log = open(archivo_de_logs_crudos, 'a')

    print('CORRIENDO RESPALDAR_SBC')
    raw_log.write('CORRIENDO RESPALDAR_SBC')

    print('Respaldando: ' + traductor[env.host_string][0])
    raw_log.write('Respaldando: ' + traductor[env.host_string][0])

    # Genero una subcarpeta por cada SBC
    subcarpeta_individual_de_sbcs = traductor[env.host_string][0] + '/'
    folder = carpeta_de_backups + subcarpeta_de_sbcs + subcarpeta_individual_de_sbcs
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Me conecto y le pido a la OSV que haga el respaldo
    with settings(user=usuario_sbc, password=password_sbc, warn_only=True):
        try:
            resultado = get(sbc_backup_path, folder)
            if resultado.succeeded:
                success_msg = traductor[env.host_string][0] + ' Succeed!\n'
                pretty_log.write(success_msg)
                pretty_log.close()
                raw_log.write(success_msg)
            else:
                raise Exception('Error al hacer scp al equipo' + traductor[env.host_string][0])
        except Exception as e:
            err_msg = 'ATENCION!!!! ' + traductor[env.host_string][0] + ' Failed!\n'
            err_msg += 'El equipo al que no se le pudo respaldar la configuracion fue: ' + traductor[env.host_string][0] + '\n'
            err_msg += 'El error fue: ' + str(e)
            try:
                subject = 'Alerta de falla en el respaldo de configuraciones.'
                body = err_msg
                send_mail(subject, body)
            except:
                err_msg += 'No se pudo enviar el mail!\n'
            pretty_log.write(err_msg)
            pretty_log.close()
            raw_log.write(err_msg)
            raw_log.write('Los paths remotos que no se pudieron descargar fueron: ' + resultado.failed)
    raw_log.close()


def respaldar_configuraciones():
    if traductor[env.host_string][1] == 'cisco':
        respaldar_cisco()
    elif traductor[env.host_string][1] == 'vyos':
        respaldar_vyos()
    elif traductor[env.host_string][1] == 'osv':
        respaldar_osv()
        #respaldar_cdr()
    elif traductor[env.host_string][1] == 'sbc':
        respaldar_sbc()