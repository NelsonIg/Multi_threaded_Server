import socket, os, json, pdb, time,sys, traceback, threading
from threading import Thread
#--------------------------------------------------------------------------------------------------
    #Client
#--------------------------------------------------------------------------------------------------

class Client:
    """ This class allwos the user to connect to a server and receive a textfile
    """
 
    #constructor + Type hinting adr:str appears whe creating object
    def __init__(self,adr: str, port: int):
        """Arguments:
            adr:  str - Name of domain or IP
            port: int _ between 0 and 65535
        """
        #test type of arguments-------------------------------------------------
        if type(port) is not int: #raise exception if port is not integer
            raise Exception('ip must be of type integer')
        elif port < 0 or port > 65535:
            raise Exception('Port must be between 0 and 65535')
        if type(adr) is not str: #raise exception if adr is not string
            raise Exception('adr must be of type String')
        #-----------------------------------------------------------------------
        self.adr     = adr
        self.port   = port

          
    def get_file(self,fileName):
        """
            Receives a file from given server
        """
        if type(fileName) is not str or fileName == '': #raise exception if adr is not string
            raise Exception('file name not of type String or empty String')
        msg = fileName
        #creat directory
        downloadtime = time.localtime(time.time())
        downloadDir = ('downloads_'+str(downloadtime[0])+'_'+
                       str(downloadtime[1])+'_'+str(downloadtime[2]))
        if os.path.isdir(downloadDir) is False:
            os.mkdir(downloadDir)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0)
        
        # resolve hostname and connect to server
        ip = socket.gethostbyname(self.adr)
        s.connect((ip,self.port))
        s.send(msg.encode())
        #msg = s.recv(4096).decode()
        recv_filelines(s,fileName,downloadDir)
        s.send(b'close')
        s.close()
        
        if msg == 'not found':
            print('\'%s\' not found by server' %(fileName))
            raise Exception('file not found by server')
            return

#--------------------------------------------------------------------------------------------------
       #Client Handler
#--------------------------------------------------------------------------------------------------

class ClientHandler(Thread):
    """ Handles socket and acception of clients as a thread:
        run(): 1. initializes server by callin socket_server_ini from module
                    'threaded_networking'
                2. accepts new clients with class FileServer from
                'threaded_networking'
    """
    def __init__(self):
        Thread.__init__(self)
        self._stop_event = threading.Event()

    def run(self):
        s = socket_server_ini('',0)
        s.settimeout(10)
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
                t.append(FileServer(c,ip,port)) 
                t[num].start()
                num = num + 1
            except:
                pass
            
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

#-------------------------------------------------------------------------------------------------
    #Server
#--------------------------------------------------------------------------------------------------
    
class FileServer(Thread):
    """
        Class sends requested file or:
            - 'not found' if requested file is not in repository
            - if 'close' is received, connection is closed.
    """
    def __init__(self, con,ip: str,port: int):
        Thread.__init__(self)
        self.ip       = ip
        self.port     = port
        self.con      = con
        self._stop_event = threading.Event()
        
       
    def run(self):
        while True:
            #check flag from self.stop()
            if self._stop_event is True:
                self.con.close()
                print('[self]:closed connection to [client %i]' %(self.port) )
                break

            #send file
            try:
                msg = self.con.recv(1028).decode()
                print('[client %i]: %s\n'%(self.port,msg))

                if msg == 'close':
                    self.con.send(b'close connection...')
                    self.con.close()
                    break
                #-------------- open and read file -----------------
                try:
                    l = read_filelines(msg)
                    send_filelines(self.con,l)
                #--------------------------------------------------
                except Exception as err:
                    traceback.print_exc()
                    msg ='not found'
                    self.con.send(msg.encode())
            except Exception as err:
                traceback.print_exc()
                break
            
    def stop(self):
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()
    
#--------------------------------------------------------------------------------------------------
    #Functions
#--------------------------------------------------------------------------------------------------
                
def read_file(fileName: str):
    fileJson = {}
    try:# textfile
        with open(fileName)as file:
            fileJson['content'] = file.read()
    except:
        try:#binary type
            with open(fileName,'rb')as file:
                fileJson['content'] = file.read().decode('cp855') #cp855 to be able to decode to string
        except: #not found
            raise Exception('file not found %s' %(fileName))
    fileJson['name'] = fileName
    return fileJson

def read_filelines(fileName: str):
    try:# textfile
        with open(fileName)as file:
             l = file.readlines()
             l = [l[x].encode() for x in range(0,len(l))] # encode each element of list
    except:
        try:#byte type
            with open(fileName,'rb')as file:
                l = file.readlines()
        except: #not found
            raise Exception('file not found %s' %(fileName))
    return l

def send_filelines(c,fileList: list):
    for x in range(0,len(fileList)):
       c.send(fileList[x])
       c.recv(1028)# client send 'ack' when received
    c.send(b'END')
    c.recv(1028)
    
def recv_filelines(s,fileName: str,downloadDir :str):
    fileList = []
    
    while True:
        line = s.recv(4096).decode('cp855')
        if line == 'not found':
            raise Exception('file not found %s' %(fileName))
        s.send(b'Ack')
        if line == 'END': break
        fileList.append(line)
    try:#txtfile
        with open(downloadDir+'/'+os.path.split(fileName)[1],'w')as file: #closes the file automatically
            file.writelines(fileList)
    except:#binaryfile
        for x in range(0,len(fileList)):
            fileList[x] = fileList[x].encode('cp855')
        with open(downloadDir+'/'+os.path.split(fileName)[1],'wb')as file: #closes the file automatically
            file.writelines(fileList)



def save_jsonfile(fileJson: dict):
    try:#txtfile
        with open(fileJson['name']+'-copy','w')as file: #closes the file automatically
            file.write(fileJson['content'])
    except:#binaryfile
        with open(fileJson['name']+'-copy','wb')as file: #closes the file automatically
            file.write(fileJson['content'].encode('cp855'))
            

def socket_server_ini(adr: str, port: int):
    """
        setup socket
    """
    #pdb.set_trace()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as err:
        traceback.print_exc()
        sys.exit()
        
    try:
        s.bind((adr,port))
    except Exception as err:
        traceback.print_exc()
        sys.exit()
    try:
        s.listen(5)
    except Exception as err:
        traceback.print_exc()
        sys.exit()
    return s
