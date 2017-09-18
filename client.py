# client.py

#!/usr/bin/env python
import sys
import httplib
import urllib
import re

def main():

    # Argument checking
    if len(sys.argv) != 5:
        print 'Enter the correct args (IP, port, X, Y)'
        return 0

    ip = sys.argv[1]
    port = sys.argv[2]
    X = sys.argv[3]
    Y = sys.argv[4]

    # Format the POST request that will be sent to the server & send it
    params = urllib.urlencode({'X': X, 'Y': Y})
    headers = {"Accept": "text/plain", "Accept-Language": "en-us,en;"}
    connection = httplib.HTTPConnection(str(ip), port)
    connection.request("POST", "FIRE", params, headers)

    # Read server's response and print to user
    response = connection.getresponse()

    data = response.read()

    print data

    hitRegex = re.compile('hit=\d')
    hitResponse = re.search(hitRegex, data).group()

    if hitResponse == 'None':
        print 'No hit data was received'
        return 0
    else:
        isHit = hitResponse[4]

    UpdateOpponentBoard(isHit, Y, X)
    UpdateHTMLOpponentBoard()

    return 0

    connection.close()

def InitiateOpponentBoard():
    opponentBoardFile = open('opponent_board.txt', 'w')
    for i in range(1,11):
        opponentBoardFile.write('__________\n')

def UpdateOpponentBoard(isHit, inY, inX):
    x = int(inX)
    y = int(inY)

    try:
        opponentBoardFile = open('opponent_board.txt', 'r')
    except:
        InitiateOpponentBoard()
        opponentBoardFile = open('opponent_board.txt', 'r')
    opponentBoard = [line for line in opponentBoardFile]

    newOpponentBoard = []

    for oldLine in range(0,10):
        newOpponentBoard.append([])
        for oldColumn in range(0,10):
            newOpponentBoard[oldLine].append(ord(opponentBoard[oldLine][oldColumn]))

    if isHit == '1':
        newOpponentBoard[y][x] = 88
    elif isHit == '0':
        newOpponentBoard[y][x] = 79
    else:
        return 1

    opponentBoardFile.close()

    newOpponentBoardFile = open('opponent_board.txt', 'w')

    for newLine in range(0,10):
        for newColumn in range(0,10):
            newCharacter = chr(newOpponentBoard[newLine][newColumn])
            newOpponentBoardFile.write(newCharacter)
        newOpponentBoardFile.write('\n')
    opponentBoardFile.close()

    return 0

def UpdateHTMLOpponentBoard():
    font = 'Consolas'

    opponentBoardFile = open('opponent_board.txt', 'r')
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

def AddSpacesIntoLine(line):
    outputLine = []

    for i in range(0,10):
        outputLine.append(line[i])
        outputLine.append(' ')
        
    return ''.join(outputLine)

if __name__ == '__main__':
    main()

