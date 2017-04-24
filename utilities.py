from datetime import datetime
import smtplib

def abrir_log():
	#Genero un archivo de logs para saber cuando falla un respaldo de configuraciones
	pretty_log = open('pretty_log.log', 'a')
	delimitador = '#############################################################################################################\n' +\
	 '############################## Corrida correspondiente a la fecha ' + str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day) + ' #################################\n' +\
	 '#############################################################################################################\n'
	pretty_log.write(delimitador)
	pretty_log.close()

def cerrar_log():
	pretty_log = open('pretty_log.log', 'a')
	delimitador = '#############################################################################################################\n' +\
	 '################################ Fin correspondiente a la fecha ' + str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day) + ' ###################################\n' +\
	 '#############################################################################################################\n' +\
	 '-------------------------------------------------------------------------------------------------------------\n\n'
	pretty_log.write(delimitador)
	pretty_log.close()


def send_alert(equipo):
	sender = 'hostedPBX@conatel.com.uy'
	receivers = ['ialmandos@conatel.com.uy']

	message = 'From: Alertas de HostedPBX <hostedPBX@contel.com.uy>\nTo: Ismael Almandos <ialmandos@conatel.com.uy>\nSubject: Alerta de falla en el respaldo de configuraciones.\n\nEquipo al que no se le pudo respaldar la configuracion: \n'
	message += str(equipo)

	try:
	   smtpObj = smtplib.SMTP('conatel-com-uy.mail.protection.outlook.com','25')
	   smtpObj.sendmail(sender, receivers, message)         
	   print "Successfully sent email"
	except SMTPException:
	   print "Error: unable to send email"