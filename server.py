# server.py

#!/usr/bin/env python
import sys
import httplib
import http.server
import urllib
import socket

def main():
   
# Argument checking
    if len(sys.argv) != 3:
        print 'Enter the correct args (port, board.txt)'
        return 0

    port = sys.argv[1]
    board = sys.argv[2]

# Create and bind the socket for the client to connect to, and then wait
    socketfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    socketfd.bind((ip, int(port)))
    socketfd.listen(1)

#   board_file = open(board, 'wb+')
#   for y in board_file:
#       for x in board_file:
#           board[y][x] = board_file.read()

# Receive data from the client in the form of an HTTP POST request
    connection, address = socketfd.accept()
    data = connection.recv(4096)
    print '-------------------- Data --------------------'
    print data
    print '----------------------------------------------'
    print 

    print '---------------- Coordinates: ----------------'
    print 
    print '----------------------------------------------'
    print
# Reply as HTTP/1.1 server, saying "HTTP OK" (code 200).
    A = 'HTTP/1.1'
    B = '200'
    C = 'OK'        
    connection.send('%s %s %s' % (A, B, C))

# Respond with a hit or miss
    print '------------------ Sending: ------------------'
    print data
    print '----------------------------------------------'
    print 
    connection.send(data)
    connection.close()

if __name__ == '__main__':
    main()

#def write_to_file(board):
#   theFile = open('board.txt', 'wb+')
#   for column in board:
#       for row in column:
#           theFile.write("%s\n" % row))

