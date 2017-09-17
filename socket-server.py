# socket-server.py

#!/usr/bin/env python
import sys
import httplib
import urllib
import socket
import re
import signal

exit = 0

def sig_handler(signum, frame):
    print 'SIG_INT handled'
    exit = 1

def main():
   
    signal.signal(signal.SIGALRM, sig_handler)

# Argument checking
    if len(sys.argv) != 3:
        print 'Enter the correct args (port, board.txt)'
        return 0

# Variable setup
    HOST = ''
    serverPort = int(sys.argv[1])
    board_file = sys.argv[2]

    file_o = open(board_file, 'r')
    board = [str(line) for line in file_o]

    # helps keep track of which ships have been sunk
    C_health = 5
    B_health = 4
    R_health = 3
    S_health = 3
    D_health = 2

# Bind the passed socket fd serverSocket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, serverPort))
    serverSocket.listen(1)

    while (exit != 1):
        print 'Ready to receive'

        connectionSocket, address = serverSocket.accept()
        data = connectionSocket.recv(2048)

        print 
        print '-------------------- Data --------------------'
        print data
        print '----------------------------------------------'
        print 

    # Store data in a linear format
        parsed_data = ''
        for i in data:
            if i != '\r' and i != '\n':
                parsed_data = parsed_data + i
            elif i == '\n':
                parsed_data + ' '
            else:
                parsed_data + ' '

    # Search parsed_data for the X=#&Y=# pattern
        Y = 10
        X = 10
        pattern = re.compile('Y=\d&X=\d')
        found = re.search(pattern, parsed_data).group()

    # Check to see that the position is valid, and if it is, fire
        sink = 'F'
        hit = 0

        if found == 'None': # No coordinates in the message
            print 'No X,Y coordinates were passed. Try again.'
            connectionSocket.send('Your X,Y coordinates did not arrive/were not found')
            connectionSocket.close()
            continue
        else:
            Y = int(found[2])
            X = int(found[6])

            if (X > 9 or Y > 9) or (X < 0 or Y < 0): # Out-of-bounds coordinates
                connectionSocket.send('X,Y coordinates out-of-bounds')
                connectionSocket.close()
                continue
            elif board[Y][X] == 'X' or board[Y][X] == '+': # Position already fired upon
                connectionSocket.send('You\'ve already fired upon that position...')
                connectionSocket.close()
                continue
            else:
            # If it's a valid position, determine if it's a hit or miss
                print "Salvo fired upon " + "[" + str(Y) + "][" + str(X) + "]\n"
                if board[Y][X] == '_':
                    print 'Miss!'
                    # How do you replace single elements of an array in python?
                    board[Y][X].replace(board[Y][X], "+")
                else:
                    hit = 1
                    print board[Y][X] + " was hit!\n"
                    # How do you replace single elements of an array in python?
                    board[Y][X].replace(board[Y][X], "X")

                    # This keeps track of what has/hasn't been sunk
                    if board[Y][X] == 'C':
                        C_health = C_health - 1
                        print 'C_health = ' + str(C_health) + "\n"
                        if C_health == 0:
                            print 'C has been sunk!!!'
                    elif board[Y][X] == 'B':
                        B_health = B_health - 1
                        print 'B_health = ' + str(B_health) + "\n"
                        if B_health == 0:
                            print 'B has been sunk!!!'
                    elif board[Y][X] == 'R':
                        R_health = R_health - 1
                        print 'R_health = ' + str(R_health) + "\n"
                        if R_health == 0:
                            print 'R has been sunk!!!'
                    elif board[Y][X] == 'S':
                        S_health = S_health - 1
                        print 'S_health = ' + str(S_health) + "\n"
                        if S_health == 0:
                            print 'S has been sunk!!!'
                    elif board[Y][X] == 'D':
                        D_health = D_health - 1
                        print 'D_health = ' + str(D_health) + "\n"
                        if D_health == 0:
                            print 'D has been sunk!!!'

    # Print the current status of the board
        print 
        print '------------------- board: -------------------'
        for i in board:
            for j in i:
                sys.stdout.write(j)
        print '----------------------------------------------'
        print 

    # Reply to the client & close connection
        message = 'HTTP /1.1 OK\r\nConnection: Close\r\n\r\nhit=' + str(hit)
        if sink != 'F':
            message = message + '&sink=' + str(sink)
        connectionSocket.send(message)
        connectionSocket.close()

    file_o.close()

if __name__ == '__main__':
    main()

