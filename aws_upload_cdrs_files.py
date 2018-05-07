from aws_utilities import upload_dir_content
from utilities import send_mail

#Upload cdr files from /home/conatel/config-backups/CDRs to AWS S3 y los borra en origen
path_cloud = "backups"
try:
    local_path = "/configs/"
    s3_prefix = "/CDRs"
    s3_prefix_osv = "/OSVs/"
    folder = "/CDRs/"
    upload_dir_content(local_path + folder, path_cloud + s3_prefix + s3_prefix_osv, True)
except Exception as e:
    print("ERROR! updating folder: " + folder + "\n")
    print("Details of error: ", e)
    send_mail("ERROR uploading folder to S3", str(e))