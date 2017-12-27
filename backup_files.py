from aws_utilities import upload_dir_content
from utilities import send_mail

path_configs = "/configs/"
path_fws = path_configs + "FWs/"
path_osvs = path_configs + "OSVs/"
path_sbcs = path_configs + "SBCs/"
path_unify = path_configs + "Unify/"
path_cloud = "backups"

try:
    upload_dir_content(path_fws, path_cloud + "/FWs/", False)
except Exception as e:
    print("ERROR! uploading folder: " + path_fws + "\n")
    print("Details of error: ", e)
    send_mail("ERROR uploading folder to S3", e)

try:
    upload_dir_content(path_osvs, path_cloud + "/OSVs/", False)
except Exception as e:
    print("ERROR! uploading folder: " + path_osvs + "\n")
    print("Details of error: ", e)
    send_mail("ERROR uploading folder to S3", e)

try:
    upload_dir_content(path_sbcs, path_cloud + "/SBCs/", False)
except Exception as e:
    print("ERROR! uploading folder: " + path_sbcs + "\n")
    print("Details of error: ", e)
    send_mail("ERROR uploading folder to S3", e)

"""
try:
    upload_dir_content(path_unify, path_cloud + "/Unify/", False)
except Exception as e:
    print("ERROR! uploading folder: " + path_unify + "\n")
    print("Details of error: ", e)
    send_mail("ERROR uploading folder to S3", e)
"""