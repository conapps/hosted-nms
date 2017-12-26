'''
Script for upload folders and files to Amazon S3 service
'''

# import SDK boto3
import boto3
# importo modulo de sistema para manipular directorios y archivos del S.O
# import system module to handle directories and files
import os
# importo sys, nos da acceso a variables del sistema
import sys
from botocore.exceptions import EndpointConnectionError, ClientError

s3 = boto3.client('s3')
# defino bucket de S3 a utilizar
bucket = 'conapps-cloud-pbx'
# defino directorio por defecto a subir
path_files = '/data/files/'


# Funcion para subir un objeto a s3 llamado file_name en la carpeta target_name


def upload_file(file_name, target_name, delete=False):
    print("Subiendo... " + target_name)
    try:
        with open(file_name, "rb") as f:
            s3.upload_fileobj(f, bucket, target_name)
            if not delete:
                return True
    except Exception as e:
        print("Hubo un error al subir el archivo: " + file_name + "\n")
        print("El error fue: ", e)
        return False
    try:
        print("Borrando... " + file_name)
        os.remove(file_name)
        return True
    except Exception as e:
        print("Hubo un error al borrar el archivo: " + file_name + "\n")
        print("El error fue: ", e)
        return False


def upload_dir_content(local_directory, cloud_directory, delete=False):
    """
    Función recursiva que dado un path (por defecto /data/files/) recorre la estructura de capretas del disco local
    local_directory y va
armando y subiendo dicha estructura de directorios y archivos en el bucket definido anteriormente en la carpeta
definida en cloud_directory
    :param file_name:
    :param target_name:
    :return:
    """
    for item in os.scandir(path=local_directory):
        if item.is_dir():
            upload_dir_content(local_directory + item.name + "/", cloud_directory + item.name + "/")
            if delete:
                print("Borrando directorio... " + item.name)
                os.rmdir(item.path)
        else:
            upload_file(local_directory + item.name, cloud_directory + item.name, delete)


if __name__ == "__main__":
    folder = os.getcwd() + "/"
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    finish = False
    response = input("Estas seguro que desea subir el directorio: " + folder + " (y or n): ")
    while not finish:
        if response.lower() == "n":
            exit()
        elif response.lower() == "y":
            finish = True
        else:
            response = input("Ingrese y or n:")
    upload_dir_content(folder, '')








