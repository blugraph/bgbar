import pysftp

private_key = "lx_sg1.pem"  # can use password keyword in Connection instead
srv = pysftp.Connection(host="52.74.191.39", username="ubuntu", private_key=private_key)
srv.chdir('/var/www/html/blunois/audio_file/')
data = srv.listdir()
print data
print srv.put('11_14_01.wav')
print "File transferred"




