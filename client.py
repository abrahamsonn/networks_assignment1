#!/usr/bin/env python
import sys
import httplib
import urllib

def main():

    if len(sys.argv) != 5:
        print 'Enter the correct args (IP, port, X, Y)'
        return 0
 
    ip = sys.argv[1]
    port = sys.argv[2]
    X = sys.argv[3]
    Y = sys.argv[4]

    params = urllib.urlencode({"X": X, "Y": Y})
    headers = {"Accept": "text/plain", "Accept-Language": "en-us,en;"}
    connection = httplib.HTTPConnection(ip, port)
    connection.request("POST", "", params, headers)
    response = connection.getresponse()

    print response.status, response.reason

    data = response.read()
    print data

if __name__ == '__main__':
    main()

