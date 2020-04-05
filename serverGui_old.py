import tkinter as tk
from tkinter import*
import subprocess

m = tk.Tk()
m.config(bg ='honeydew3')
m.title('Server')

process = False

def start():
    global process
    if process == False:
        textConsole.delete(1.0, END)
        global p
        p = subprocess.Popen(['python','send_test.py'])
        textConsole.insert(INSERT, 'Process started\n')
        process = True
def stop():
    global process
    if process == True:
        textConsole.delete(1.0, END)
        p.kill()
        textConsole.insert(INSERT, 'Process killed\n')
        process = False
def close():
    global process
    if process == True: #check if process was called
        p.kill()
    m.destroy()

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
