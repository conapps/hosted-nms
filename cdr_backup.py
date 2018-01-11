import os

importiert_folder = '/importiert'
received_archive_folder = '/received_archive'

credentials_file = '/root/.credentials'

backup_cdr_root = '/cdr-backups/'

print ('Starting files copy from : //' + importiert_folder + " folder")
os.system("cp -v " + importiert_folder + "/*.cdr " + backup_cdr_root)
print ('Finishing files copy from : //' + importiert_folder + " folder: ")

print ('Starting files copy from  : //' + received_archive_folder + " folder")
os.system("cp -v " + received_archive_folder + "/*.cdr " + backup_cdr_root)
print ('Finishing files copy from : //' + received_archive_folder + " folder")