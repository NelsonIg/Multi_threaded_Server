import socket, pdb, time
import tkinter as tk
from threading import Thread
import threading
import threaded_networking

#Functions for GUI buttons
serverOn = False
global top
def start():
    global top,serverOn
    if serverOn is False:
        textConsole.delete(1.0, tk.END)
        top = threaded_networking.ClientHandler()
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

