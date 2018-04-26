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

#Upload cdr files from Accounting server to AWS S3 [NO SE UTILIZA MAS]
#try:
#    local_path = "/cdr-backups"
#    s3_prefix = "/CDRs"
#    s3_prefix_accounting = "/Accounting"
#    folder = "/importiert/"
#    upload_dir_content(local_path + folder, path_cloud + s3_prefix + s3_prefix_accounting + folder, True)
#    folder = "/received_archive/"
#    upload_dir_content(local_path + folder, path_cloud + s3_prefix + s3_prefix_accounting + folder, True)
#except Exception as e:
#    print("ERROR! uploading folder: " + folder + "\n")
#    print("Details of error: ", e)
#    send_mail("ERROR uploading folder to S3", str(e))


#Upload cdr files from OSVs servers to AWS S3
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



path_cloud = "certificados"

#Upload CA certificates to AWS S3
try:
    path_configs = "/configs/"
    folder = "/CA/"
    upload_dir_content(path_configs + folder, path_cloud + folder, False)
except Exception as e:
    print("ERROR! uploading folder: " + folder + "\n")
    print("Details of error: ", e)
    send_mail("ERROR uploading folder to S3", str(e))