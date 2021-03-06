import tkinter as tk
from tkinter import*
import threaded_networking
import pdb, time

m = tk.Tk() #where m is the name of the main window object
m.resizable(0,0) #window not resizable 
m.config(bg ='honeydew3')
m.title('Client')

def file_request():
    #pdb.set_trace()
    textConsole.delete('1.0',END)
    
    try:
        c = threaded_networking.Client(entryIp.get(),int(entryPort.get()))
        t1 = time.time()
        file = c.get_file(entryFile.get())
        t2 = time.time()
        tdif = t2-t1
        #textConsole.insert(INSERT, 'file received\ntime needed: '+str(round(t2-t1,3))+' seconds')
        textConsole.insert(INSERT, f'file received\ntime needed: {int(tdif//60)} min {round(tdif%60,3)} sec')
    except Exception as err:
        textConsole.insert(INSERT, err)
        print(err)
        return
    
var = tk.StringVar()
entryIp = tk.Entry(m)
entryIp.grid(row = 0, column = 1,padx = 4, pady = 4)
entryIp.config( font =('arial','10','bold'))

entryPort = tk.Entry(m)
entryPort.grid(row = 1, column = 1,padx = 4, pady = 4)
entryPort.config( font =('arial','10','bold'))

entryFile = tk.Entry(m)
entryFile.grid(row = 2, column = 1,padx = 4, pady = 4)
entryFile.config( font =('arial','10','bold'))

labelIp = tk.Label(m, text = 'Ip Address:')
labelIp.grid(row = 0, column = 0,padx = 4, pady = 4)
labelIp.config(bg ='honeydew3', font =('arial','10','bold'))

labelInfo = tk.Label(m, text = 'Port:')
labelInfo.grid(row = 1, column = 0,padx = 4, pady = 4)
labelInfo.config(bg ='honeydew3', font =('arial','10','bold'))

labelInput = tk.Label(m, text = 'Enter filename:')
labelInput.grid(row = 2, column = 0,padx = 4, pady = 4)
labelInput.config(bg ='honeydew3', font =('arial','10','bold'))

buttonSend = tk.Button(m, text='connect',width=25,height = 10,command= file_request,
                       bg='olivedrab1',activebackground ='olivedrab2', bd = 4, font = ('arial','10','bold'))
buttonSend.grid(row = 0, column = 3,padx = 10, pady = 4,rowspan = 4)

buttonDestroy = tk.Button(m, text='close',width=25,height = 10,command=m.destroy,
                           bg='goldenrod',activebackground ='dark goldenrod', bd = 4, font = ('arial','10','bold'))
buttonDestroy.grid(row = 4, column = 3,padx = 10, pady = 4,rowspan = 4)


textConsole = tk.Text(m,width = 35, height = 8, bg ='snow2')
textConsole.grid(row = 4, column = 0,padx = 10, pady = 10, rowspan = 2, columnspan = 2)
textConsole.config(bd = 4, font =('arial','10','bold'))



m.mainloop()
