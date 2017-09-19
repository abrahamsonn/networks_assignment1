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

def updateBoard(char, Y, X, board):
    empty_board = [ [ None for y in range( 11 ) ] for x in range( 10 ) ]

    for x in range(0, 10):
        for y in range(0, 10):
            if x == X and y == Y:
                empty_board[y][x] = char
            else:
                empty_board[y][x] = board[y][x]

        empty_board[x][10] = '\n'

    return empty_board

def writeToFile(board):
# Write the board to file titled MYboard.html
    outBoard_f = open('board.txt', 'w+')
    outBoard_f.write("<!DOCTYPE html><html><body>")
    for y in range(0, 10):
        for x in range(0, 11):
            outBoard_f.write(' ' + board[y][x] + ' |')

        outBoard_f.write("<br>------------------------------------------------------<br>|")

    outBoard_f.write("</body></html>")

    outBoard_f.close()

def main():
   
    #signal.signal(signal.SIGALRM, sig_handler)

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

    while (True):
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

        if re.search('POST FIRE', parsed_data) != None:
        # Search parsed_data for the X=#&Y=# pattern
            Y = 10
            X = 10
            pattern = re.compile('Y=\d+&X=\d+')
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
                line = re.split('&', found)
                print line
                y = re.split('=', line[0])
                Y = int(y[1])
                x = re.split('=', line[1])
                X = int(x[1])

                print Y
                print X

                if (X > 9 or Y > 9) or (X < 0 or Y < 0): # Out-of-bounds coordinates
                    print 'X,Y coordinates out-of-bounds'
                    connectionSocket.send('X,Y coordinates out-of-bounds')
                    connectionSocket.close()
                    continue
                elif board[Y][X] == 'X' or board[Y][X] == 'O': # Position already fired upon
                    print 'You\'ve already fired upon that position...'
                    connectionSocket.send('You\'ve already fired upon that position...')
                    connectionSocket.close()
                    continue
                else:
                # If it's a valid position, determine if it's a hit or miss
                    print "Salvo fired upon " + "[" + str(Y) + "][" + str(X) + "]\n"
                    if board[Y][X] == '_':
                        print 'Miss!'
                        # How do you replace single elements of an array in python?
                        board = updateBoard('O', Y, X, board)
                    else:
                        hit = 1
                        print board[Y][X] + " was hit!\n"
                        # How do you replace single elements of an array in python?
                        board = updateBoard('X', Y, X, board)

                        # This keeps track of what has/hasn't been sunk
                        if board[Y][X] == 'C':
                            C_health = C_health - 1
                            print 'C_health = ' + str(C_health) + "\n"
                            if int(C_health) == 0:
                                print 'C has been sunk!!!'
                        elif board[Y][X] == 'B':
                            B_health = B_health - 1
                            print 'B_health = ' + str(B_health) + "\n"
                            if int(B_health) == 0:
                                print 'B has been sunk!!!'
                        elif board[Y][X] == 'R':
                            R_health = R_health - 1
                            print 'R_health = ' + str(R_health) + "\n"
                            if int(R_health) == 0:
                                print 'R has been sunk!!!'
                        elif board[Y][X] == 'S':
                            S_health = S_health - 1
                            print 'S_health = ' + str(S_health) + "\n"
                            if int(S_health) == 0:
                                print 'S has been sunk!!!'
                        elif board[Y][X] == 'D':
                            D_health = D_health - 1
                            print 'D_health = ' + str(D_health) + "\n"
                            if int(D_health) == 0:
                                print 'D has been sunk!!!'

        # Print the current status of the board
            print 
            print '------------------- board: -------------------'
            for i in board:
                for j in i:
                    sys.stdout.write(str(j))
            print '----------------------------------------------'
            print 
            writeToFile(board)

        # Reply to the client & close connection
            message = 'HTTP /1.1 OK\r\nConnection: Close\r\n\r\nhit=' + str(hit)
            if sink != 'F':
                message = message + '&sink=' + str(sink)
            connectionSocket.send(message)
            connectionSocket.close()

        elif re.search('GET', parsed_data):
            fileNameToSend = []

            if re.search('own_board.html', parsed_data):
                fileNameToSend.append('own_board.html')
            elif re.search('opponent_board.html', parsed_data):
                UpdateHTMLOpponentBoard()
                fileNameToSend.append('opponent_board.html')
            else:
                fileNameToSend.append('-1')

            sendStatus = SendBoard(fileNameToSend[0], connectionSocket)
            print '------------------- GET ----------------------'
            print sendStatus
            print '----------------------------------------------'

            connectionSocket.close()

        UpdateHTMLOwnBoard()

    file_o.close()

def UpdateHTMLOwnBoard():
    font = 'Consolas'

    ownBoardFile = open('board.txt', 'r')
    ownBoardHTML = open('own_board.html', 'w')

    ownBoardHTML.write('<html><title>Own Board</title><body>\n')
    ownBoardHTML.write(
        '<font face = "'
        + font
        + '" size = "5">&nbsp 0 1 2 3 4 5 6 7 8 9 X</font><br />')
    lineNumber = 0
    for line in ownBoardFile:
        spacedLine = AddSpacesIntoLine(line)
        ownBoardHTML.writelines(
            '<font face = "'
            + font
            + '" size = "5">'
            + str(lineNumber)
            + ' '
            + spacedLine
            + '</font><br />')
        lineNumber = lineNumber + 1
    ownBoardHTML.write(
        '<font face = "'
        + font
        + '" size = "5">Y</font><br /></body></html>')

    ownBoardFile.close()
    ownBoardHTML.close()


def UpdateHTMLOpponentBoard():
    font = 'Consolas'

    try:
        opponentBoardFile = open('opponent_board.txt', 'r')
    except:
        opponentBoardFile = InitiateOpponentBoard()
    opponentBoardHTML = open('opponent_board.html', 'w')

    opponentBoardHTML.write('<html><title>Opponent\'s Board</title><body>\n')
    opponentBoardHTML.write(
        '<font face = "'
        + font
        + '" size = "5">&nbsp 0 1 2 3 4 5 6 7 8 9 X</font><br />')
    lineNumber = 0
    for line in opponentBoardFile:
        spacedLine = AddSpacesIntoLine(line)
        opponentBoardHTML.writelines(
            '<font face = "'
            + font
            + '" size = "5">'
            + str(lineNumber)
            + ' '
            + spacedLine
            + '</font><br />')
        lineNumber = lineNumber + 1
    opponentBoardHTML.write(
        '<font face = "'
        + font
        + '" size = "5">Y</font><br /></body></html>')

    opponentBoardFile.close()
    opponentBoardHTML.close()

def InitiateOpponentBoard():
    opponentBoardFile = open('opponent_board.txt', 'w')
    for i in range(1,11):
        opponentBoardFile.write('__________\n')
def AddSpacesIntoLine(line):
    outputLine = []

    for i in range(0,10):
        outputLine.append(line[i])
        outputLine.append(' ')
        
    return ''.join(outputLine)

def SendBoard(boardName, connectionSocket):
    statuses = [
        '200 OK',
        '400 Bad Request',
        '404 Not Found'
        ]

    status = 0
    if boardName == '-1':
        status = 1

    try:
        
        try:
            openedBoardFile = open(boardName, 'rb')
        except:
            status = 2
        boardHTML = openedBoardFile.read(1024)

        connectionSocket.send(
            'HTTP/1.1'
            + statuses[status]
            + '\r\nContent-Type: text/html; \r\n\r\n'
            + boardHTML)

        return boardName + ' transmission has succeeded.'
    except:
        return boardName + ' transmission has failed.'

if __name__ == '__main__':
    main()

