import pickle
import os
from shutil import copyfile
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

if not os.path.isfile("settings.py"):
    copyfile("settings.py.example", "settings.py")
from settings import HIVEPORT, AUTHORISEDBEARS
from arguments import parse
from myenc import AESCipher


def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', HIVEPORT))
    serverSocket.listen(1)
    try:
        with file('temp.db') as f:
            stringfile = f.read()
        db = pickle.loads(stringfile)
    except:
        db = list()
    print "Awaiting for bears on port %s" % HIVEPORT
    while True:
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(30000)
            request = message.split(":")
            key = AUTHORISEDBEARS[request[0]]
            deciper = AESCipher(key)
            data = pickle.loads(deciper.decrypt(request[1]))
            print data
            db.append(data)
            with open('temp.db', "w") as f:
                f.write(str(pickle.dumps(data)))
            connectionSocket.send("200")
            connectionSocket.close()
        except:
            connectionSocket.send("300")
            connectionSocket.close()
    serverSocket.close()

if __name__ == '__main__':
    args = parse()
    main()
