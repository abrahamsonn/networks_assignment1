# socket-server.py

#!/usr/bin/env python
import sys
import httplib
import urllib
import socket
import re

def main():
   
# Argument checking
    if len(sys.argv) != 3:
        print 'Enter the correct args (port, board.txt)'
        return 0

# Variable setup
    HOST = ''
    serverPort = int(sys.argv[1])
    board = sys.argv[2]

# Bind the passed socket fd serverSocket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, serverPort))
    serverSocket.listen(1)

    print 'Ready to receive'

    connectionSocket, address = serverSocket.accept()
    data = connectionSocket.recv(2048)

    print 
    print '-------------------- Data --------------------'
    print data
    print
    for i in range(len(data)):
        sys.stdout.write(data[i])
        sys.stdout.write(' ')
    print
    print '----------------------------------------------'
    print 


# Search data for the X=#&Y=# pattern
    pattern = re.compile('(X=\d+&Y=\d+)\|(Y=\d+&X=\d+)')
    print pattern.match(data)

# Prinnt special data
    print 
    print '---------------- Parsed data:  ---------------'
    for i in data:
        if i != '\n':
            sys.stdout.write(i)
        elif i == '\n':
            sys.stdout.write(' ')
        else:
            sys.stderr.write("unkown char\n")
    print
    print '----------------------------------------------'
    print 

# Reply to the client & close connection
    connectionSocket.send('i hear you fa shizzle')
    connectionSocket.close()

if __name__ == '__main__':
    main()
