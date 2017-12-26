'''
Scritp para subir directorios y archivos a AWS S3
'''

#importo boto3 SDK de AWS para python
import boto3
#importo modulo de sistema para manipular directorios y archivos del S.O
import os
#importo sys, nos da acceso a variables del sistema
import sys



s3 = boto3.client('s3')
#defino bucket de S3 a utilizar
bucket = 'conapps-cloud-pbx'
#defino directorio por defecto a subir
path_files = '/data/files/'

#Funcion para subir un objeto a s3 llamado file_name en la carpeta target_name
def upload_file(file_name,target_name):
    print("Subiendo... " + target_name)
    with open(file_name, "rb") as f:
        s3.upload_fileobj(f, bucket, target_name)


'''
Función recursiva que dado un path por defecto /data/files/
recorre la estructura de capretas del disco local local_directory y va
armando y subiendo dicha estructura de directorios y archivos en el bucket definido
anteriormente
'''
def upload_dir_content(local_directory, cloud_directory):
    #actual_path = local_directory + cloud_directory
    for item in os.scandir(path=local_directory):
        if item.is_dir():
            upload_dir_content(local_directory + item.name + "/", cloud_directory + item.name + "/")
        else:
            upload_file(local_directory + item.name, cloud_directory + item.name)



if __name__ == "__main__":
    dir = os.getcwd() + "/"
    if len(sys.argv) > 1:
        dir = sys.argv[1]
    finish = False
    response = input("Estas seguro que desea subir el directorio: " + dir + " (y or n): ")
    while not finish:
        if response.lower() == "n":
            exit()
        elif response.lower() == "y":
            finish = True
        else:
            response = input("Ingrese y or n:")
    upload_dir_content(dir, '')



"""
[]
#main programl
for item in os.scandir(path=path_files):
    if item.is_dir():
        print("Entrando a nuevo directorio: " + item.name)
        relative_path = path_files + item.name + "/"
        for other_item in os.scandir(path=relative_path):
                
    else:
        upload_file(path_files + item.name, item.name)






for item in os.scandir(path="/data/files"):
    if item.is_dir():
        print("Ignorando directorio: " + item.name)
    else:
        print("Subiendo... " + item.name)
        s3.upload_file(path_files + item.name, bucket, item.name)
"""
 #s3.Object('conapps-cloud-pbx', 'ejemplo.txt').put(Body=open('/data/ejemplo.txt','rb'))






