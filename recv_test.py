import socket
import json, time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10.0)
ip = socket.gethostbyname('127.0.0.1')
s.connect((ip,23))
print('connected')

while True:

    msg = input('[self]: Enter filename:\n')
    while msg == '':
        msg = input('[self]: Enter filename:\n')
    s.send(msg.encode())
    if msg == 'close':
        s.close()
        #print('[self]: connection closed\n')
        #time.sleep(5)
        break
    msg = s.recv(1028).decode()

    if msg == 'not found':
        print('[server]:',msg)
    else:
        print(msg,'\n')
        try:
            fileJson = json.loads(msg)
            print(fileJson['content'])
        except Exception:
            print('[self]: file could not be loaded\n')
            pass
    
 

