import os

mnt_dest_cdr_osv1 = '/mnt-folder-osv1'
mnt_dest_cdr_osv2 = '/mnt-folder-osv2'
remote_cdr_osv1 = '/osv1'
remote_cdr_osv2 = '/osv2'


credentials_file = '/root/.credentials'

accouting_ip = '172.16.0.105'

backup_cdr_root = '/cdr-backups'


print('Mounting remote folder //' + accouting_ip + remote_cdr_osv1 + ' in ' + mnt_dest_cdr_osv1 + '')
os.system("mount -t cifs -o credentials=" + credentials_file + " //" + accouting_ip + remote_cdr_osv1 + " " +
          mnt_dest_cdr_osv1 + "")

print ('Starting files copy from : //' + accouting_ip + " folder: " + remote_cdr_osv1)
os.system("cp -v " + mnt_dest_cdr_osv1 + "/* " + backup_cdr_root + "")
print ('Finishing files copy from : //' + accouting_ip + " folder: " + remote_cdr_osv1)

print('Unmounting remote folder //' + accouting_ip + remote_cdr_osv1 + '')
os.system("umount " + mnt_dest_cdr_osv1 + "/")


print('Mounting remote folder //' + accouting_ip + remote_cdr_osv2 + ' in ' + mnt_dest_cdr_osv2 + '')
os.system("mount -t cifs -o credentials=" + credentials_file + " //" + accouting_ip + remote_cdr_osv2 + " " +
          mnt_dest_cdr_osv2 + "")

print ('Starting files copy from  : //' + accouting_ip + " folder: " + remote_cdr_osv2)
os.system("cp -v " + mnt_dest_cdr_osv2 + "/* " + backup_cdr_root + "")
print ('Finishing files copy from : //' + accouting_ip + " folder: " + remote_cdr_osv2)

print('Unmounting remote folder //' + accouting_ip + remote_cdr_osv2 + '')
os.system("umount " + mnt_dest_cdr_osv2 + "/")

input("Done!...")
