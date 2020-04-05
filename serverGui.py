import socket, pdb, threaded_networking, time
import tkinter as tk
from threading import Thread
import threading


class start_server(Thread):
    """Handles socket and acception of clients as a thread"""
    def __init__(self):
        Thread.__init__(self)
        self._stop_event = threading.Event()

    def run(self):
        s = threaded_networking.socket_server_ini('',0)
        s.settimeout(5)
##        print('Server started:\n Host: %s\n Port: %i'
##              %(socket.gethostbyname(socket.gethostname()),s.getsockname()[1]))
        self.hostIp = socket.gethostbyname(socket.gethostname())
        self.port   = s.getsockname()[1]

        t = [] #list of threads
        num = 0
        while True:
            if self.stopped() is True:
                for x in range(0,len(t)):
                    t[x].stop()
                    t[x].join()
                s.close()
                print('server closed')
                return
                
            try:
                (c,(ip,port)) = s.accept() #accept() returns (socket,(Ip,port))
                print('new connection %s %i'%(ip,port))
                # fill list with threads
                t.append(threaded_networking.ServerSendFile(c,ip,port)) 
                t[num].start()
                num = num + 1
            except:
                pass
            
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


#Functions for GUI buttons
serverOn = False
global top
def start():
    global top,serverOn
    if serverOn is False:
        textConsole.delete(1.0, tk.END)
        top = start_server()
        top.start()
        time.sleep(1)
        textConsole.insert(tk.INSERT, 'Server started:\n' + 'IP: ' +
                           top.hostIp +'\nPort: ' + str(top.port)+'\n')
        serverOn = True
    else:
        textConsole.insert(tk.INSERT, 'Server already started:\n' + 'IP: ' +
                           top.hostIp +'\nPort: ' + str(top.port)+'\n')
def stop():
    global top, serverOn
    if serverOn is True:
        top.stop()
        top.join()
        textConsole.insert(tk.INSERT, 'Server closed\n')
        serverOn = False
    else:
        textConsole.insert(tk.INSERT, 'no Server to close\n')

def close():
    global top, serverOn
    if serverOn is True:
        top.stop()
        top.join()
    m.destroy()
#Layout of User Interface
m = tk.Tk()
m.config(bg ='honeydew3')
m.title('Server')

buttonStart = tk.Button(m, text='start',width=20,height = 10,command= start,
                        bg='olivedrab1',activebackground ='olivedrab2', bd = 4, font = ('arial','10','bold'))
buttonStart.grid(row = 0, column = 3,padx = 10, pady = 10)

buttonStop = tk.Button(m, text='stop',width=20,height = 10,command= stop,
                       bg='salmon2',activebackground ='salmon3', bd = 4, font = ('arial','10','bold'))
buttonStop.grid(row = 1, column = 3,padx = 10, pady = 10)

buttonDestroy = tk.Button(m, text='close',width=20,height = 10,command=close,
                          bg='goldenrod',activebackground ='dark goldenrod', bd = 4, font = ('arial','10','bold'))
buttonDestroy.grid(row = 2, column = 3,padx = 10, pady = 10)

textConsole = tk.Text(m,width = 30, height = 32, bg ='snow2')
textConsole.config(bd = 4,font =('arial','10','bold'))
textConsole.grid(row = 0, column = 0,padx = 10, pady = 0, rowspan = 4,
                 columnspan = 3)
m.mainloop()

