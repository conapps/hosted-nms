from aws_utilities import upload_dir_content
from utilities import send_mail

path_cloud = "backups"

#Upload configurations backups to AWS S3
try:
    path_configs = "/configs/"
    folder = "/FWs/"
    upload_dir_content(path_configs + folder, path_cloud + folder, True)
    folder = "/OSVs/"
    upload_dir_content(path_configs + folder, path_cloud + folder, False)
    folder = "/SBCs/"
    upload_dir_content(path_configs + folder, path_cloud + folder, False)
    #folder = "/Unify/"
    #upload_dir_content(path_configs + folder, path_cloud + folder, False)
except Exception as e:
    print("ERROR! uploading folder: " + folder + "\n")
    print("Details of error: ", e)
    send_mail("ERROR uploading folder to S3", str(e))

#Uplado cdr backups to AWS S2
try:
    path_configs = "/cdr-backups/"
    folder = "/CDR-Backups/"
    upload_dir_content(path_configs, path_cloud + folder, True)
except Exception as e:
    print("ERROR! uploading folder: " + folder + "\n")
    print("Details of error: ", e)
    send_mail("ERROR uploading folder to S3", str(e))
