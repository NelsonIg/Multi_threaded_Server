import tkinter as tk
from tkinter import*
import threaded_networking
import pdb

m = tk.Tk() #where m is the name of the main window object
m.title('Client')

def file_request():
    #pdb.set_trace()
    textConsole.delete('1.0',END)
    
    try:
        c = threaded_networking.Client('localhost',int(entryPort.get()))      
        file = c.get_file(entryFile.get())      
        textConsole.insert(INSERT, 'file received')
    except Exception as err:
        textConsole.insert(INSERT, err)
        print(err)
        return
    
var = tk.StringVar()
entryFile = tk.Entry(m)
entryFile.grid(row = 0, column = 1,padx = 4, pady = 4)

entryPort = tk.Entry(m)
entryPort.grid(row = 1, column = 1,padx = 4, pady = 4)

labelInfo = tk.Label(m, text = '127.0.0.1, Port:')
labelInfo.grid(row = 1, column = 0,padx = 4, pady = 4)

labelInput = tk.Label(m, text = 'Enter filename:')
labelInput.grid(row = 0, column = 0,padx = 4, pady = 4)

buttonSend = tk.Button(m, text='connect',width=25,command= file_request)
buttonSend.grid(row = 0, column = 3,padx = 4, pady = 4)

buttonDestroy = tk.Button(m, text='close',width=25,command=m.destroy)
buttonDestroy.grid(row = 4, column = 3,padx = 4, pady = 4)


textConsole = tk.Text(m,width = 45, height = 5,bg ='snow2')
textConsole.grid(row = 2, column = 0,padx = 0, pady = 4, columnspan = 2,)



m.mainloop()
