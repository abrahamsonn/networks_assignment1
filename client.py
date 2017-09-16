# client.py

#!/usr/bin/env python
import sys
import httplib
import urllib

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
    print '-------------------- Data --------------------'
    print data
    print '----------------------------------------------'

    print

    print '-------------- response.status ---------------'
    print response.status 
    print '----------------------------------------------'

    print

    print '-------------- response.reason ---------------'
    print response.reason # OK
    print '----------------------------------------------'

    print

    connection.close()

if __name__ == '__main__':
    main()

