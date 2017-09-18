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

    UpdateKnowledgeBoard(isHit, Y, X)

    return 0

    connection.close()

def InitiateKnowledgeBoard():
    knowledgeBoardFile = open('knowledgeBoard.txt', 'w')
    for i in range(1,11):
        knowledgeBoardFile.write('__________\n')

def UpdateKnowledgeBoard(isHit, inY, inX):
    x = int(inX)
    y = int(inY)

    try:
        print 'try this'
        knowledgeBoardFile = open('knowledgeBoard.txt', 'r')
    except:
        InitiateKnowledgeBoard()
        knowledgeBoardFile = open('knowledgeBoard.txt', 'r')
    knowledgeBoard = [line for line in knowledgeBoardFile]

    newKnowledgeBoard = []

    for oldLine in range(0,10):
        newKnowledgeBoard.append([])
        for oldColumn in range(0,10):
            newKnowledgeBoard[oldLine].append(ord(knowledgeBoard[oldLine][oldColumn]))

    if isHit == '1':
        newKnowledgeBoard[y][x] = 88
    elif isHit == '0':
        newKnowledgeBoard[y][x] = 79
    else:
        return 1

    knowledgeBoardFile.close()

    newKnowledgeBoardFile = open('knowledgeBoard.txt', 'w')

    for newLine in range(0,10):
        for newColumn in range(0,10):
            newCharacter = chr(newKnowledgeBoard[newLine][newColumn])
            newKnowledgeBoardFile.write(newCharacter)
        newKnowledgeBoardFile.write('\n')
    knowledgeBoardFile.close()

    return 0

if __name__ == '__main__':
    main()

