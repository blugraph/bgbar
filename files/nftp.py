from ftplib import FTP_TLS

ftps = FTP_TLS(host='52.74.191.39', user='ubuntu', passwd='', keyfile='lx_sg1.pem', timeout=10)
ftps.login()           # login anonymously before securing control channel
ftps.prot_p()          # switch to secure data connection.. IMPORTANT! Otherwise, only the user and password is encrypted and not all the file data.
ftps.retrlines('LIST')

filename = 'remote_filename.bin'
print 'Opening local file ' + filename
myfile = open(filename, 'wb')

ftps.retrbinary('RETR %s' % filename, myfile.write)

ftps.close()

