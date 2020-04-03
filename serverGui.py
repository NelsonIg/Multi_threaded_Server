import tkinter as tk
from tkinter import*
import subprocess

#global m
m = tk.Tk()
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
    
buttonStop = tk.Button(m, text='stop',width=25,command= stop)
buttonStop.grid(row = 1, column = 3,padx = 0, pady = 4)

buttonStart = tk.Button(m, text='start',width=25,command= start)
buttonStart.grid(row = 0, column = 3,padx = 0, pady = 4)

buttonDestroy = tk.Button(m, text='close',width=25,command=close)
buttonDestroy.grid(row = 3, column = 3,padx = 0, pady = 4)

textConsole = tk.Text(m,width = 20, height = 5, bg ='snow2')
textConsole.grid(row = 0, column = 0,padx = 0, pady = 0, rowspan = 4)
m.mainloop()
