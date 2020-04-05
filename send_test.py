import socket, pdb, threaded_networking
import tkinter as tk
from threading import Thread
#pdb.set_trace()

s = threaded_networking.socket_server_ini('',0)
print('Server started:\n Host: %s\n Port: %i'
      %(socket.gethostbyname(socket.gethostname()),s.getsockname()[1]))

while True:
    try:
        (c,(ip,port)) = s.accept() #accept() returns (socket,(Ip,port))
    except Exception as err:
        err
    print('new connection %s %i'%(ip,port))
    t = threaded_networking.ServerSendFile(c,ip,port)
    t.start()
    input('Enter to stop')
    t.stop()
    while True:
        if t.stopped:
            print('stopped')
            break
    print(t.isAlive())

    break
