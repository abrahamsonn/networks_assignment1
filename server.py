#!/usr/bin/env python
import sys
import httplib
import urllib
import socket

def main():
   
    if len(sys.argv) != 4:
        print 'Enter the correct args (IP, port, board.txt)'
        return 0

    ip = sys.argv[1]
    port = sys.argv[2]
    board = sys.argv[3]

    socketfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    socketfd.bind((ip, int(port)))
#    socketfd.bind(('127.0.0.1', 11111))
    socketfd.listen(1)

#   board_array = [10][10]

#   board_file = open(board, 'wb+')
#   for y in board_file:
#       for x in board_file:
#           board[y][x] = board_file.read()

    connection, address = socketfd.accept()
    data = connection.recv(50)
    print data
    connection.send(data)
    connection.close()

if __name__ == '__main__':
    main()

#def write_to_file(board):
#   theFile = open('board.txt', 'wb+')
#   for column in board:
#       for row in column:
#           theFile.write("%s\n" % row))

