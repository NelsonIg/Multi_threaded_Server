import socket, pdb, threaded_networking
import tkinter as tk
from threading import Thread
#pdb.set_trace()

s = threaded_networking.socket_server_ini('',23)

while True:
    try:
        (c,(ip,port)) = s.accept() #accept() returns (socket,(Ip,port))
    except Exception as err:
        err
    print('new connection %s %i'%(ip,port))
    newThread = threaded_networking.ServerSendFile(c,ip,port)
    newThread.start()
