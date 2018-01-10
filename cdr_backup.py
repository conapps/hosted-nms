import os

mnt_dest_cdr_osv1 = '/mnt-folder-osv1'
mnt_dest_cdr_osv2 = '/mnt-folder-osv2'
remote_cdr_osv1 = '/osv1'
remote_cdr_osv2 = '/osv2'

sub_folder_backup_osv1 = '/osv1'
sub_folder_backup_osv2 = '/osv2'
credentials_file = '/root/.credentials'

backup_cdr_root = '/cdr-backups/'

print ('Starting files copy from : //' + mnt_dest_cdr_osv1 + " folder: " + remote_cdr_osv1)
os.system("cp -v " + mnt_dest_cdr_osv1 + "/* " + backup_cdr_root)
print ('Finishing files copy from : //' + mnt_dest_cdr_osv1 + " folder: " + remote_cdr_osv1)

print ('Starting files copy from  : //' + mnt_dest_cdr_osv2 + " folder: " + remote_cdr_osv2)
os.system("cp -v " + mnt_dest_cdr_osv2 + "/* " + backup_cdr_root)
print ('Finishing files copy from : //' + mnt_dest_cdr_osv2 + " folder: " + remote_cdr_osv2)