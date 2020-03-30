import socket, os, json, pdb, time,sys
from threading import Thread



def socket_server_ini(adr: str, port: int):
    """
        setup socket
    """
    #pdb.set_trace()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as err:
        print('socket.socket(socket.AF_INET, socket.SOCK_STREAM)',err)
        sys.exit()
        
    try:
        s.bind((adr,port))
    except Exception as err:
        print('s.bind((adr,port))',err)
        sys.exit()
    try:
        s.listen(5)
    except Exception as err:
        print('s.listen(5)',err)
        sys.exit()
    return s

class ServerSendFile(Thread):
    """
        Class sends requested file or:
            - 'not found' if requested file is not in repository
            - if 'close' is received, connection is closed.
    """
    def __init__(self, con,ip: str,port: int):
        self.ip       = ip
        self.port     = port
        self.con      = con
        Thread.__init__(self)
       
    def run(self):
        while True:
            try:
                msg = self.con.recv(1028).decode()
                print('[client %i]: %s\n'%(self.port,msg))

                if msg == 'close':
                    self.con.send(b'close connection...')
                    self.con.close()
                    break
                #-------------- open and read file -----------------
                fileJson ={}
                try:
                    file = open(msg,'r')
                    fileJson['name'] = msg
                    fileJson['content'] = file.read()
                    file.close()
                    msg = json.dumps(fileJson)
                    self.con.send(msg.encode())
                #--------------------------------------------------
                except Exception as err:
                    msg ='not found'
                    self.con.send(msg.encode())
            except Exception as err:
                print(err)
                break
                
