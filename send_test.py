import socket, pdb, threaded_networking
#pdb.set_trace()

s = threaded_networking.socket_server_ini('',23)


while True:
    (c,(ip,port)) = s.accept() #accept() returns (socket,(Ip,port))
    print('new connection %s %i'%(ip,port))
    newThread = threaded_networking.ServerSendFile(c,ip,port)
    newThread.start()
