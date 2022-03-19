#!/usr/bin/env python
import os, datetime, threading, sys, time
from socket import *

BYTES_TO_RECEIVE = 1024
SCRIPT_LOCATION = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
SERVER_PORT = int(sys.argv[1])

# Enabled Multi threding

class myThread (threading.Thread):
    def __init__(self, threadID, name, connectionsocket):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.connectionSocket = connectionsocket
    def run(self):
        initial_time = time.time() #Store the time when request is sent
        handleNewConnection(self.name, self.connectionSocket)
        ending_time = time.time() #Time when acknowledged the request
        elapsed_time = str(ending_time - initial_time)
        print('The Round Trip Time is {}'.format(elapsed_time))
        print('Hostname of the server: ' + gethostname())
        print('Socket IP:' + str(AF_INET))

# Form the HTTP header response to be sent to the client
def formHeaderResponse():
    response = ("HTTP/1.1 200 Ok\r\n\r\n")
    return response

# Form the HTTP response of the requested to be sent to the client
def webPageResponse(wpSize, wpName):
    responseHeader = ("HTTP/1.1 200 OK\r\n"
                "Date: " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\r\n"
                "Server: ChanikyaServer/0.1\r\n"
                "Content-Length: " + str(wpSize) + "\r\n"
                "Content-Type: text/html\r\n"
                "Connection: Closed\r\n\r\n")
    return responseHeader

# Form the HTTP 404 response to be sent to the client
def serve404Response(filename, isGetRequest):
    html = ("<h1><center>Error 404: File not found!</h1><br>"
            "<center>File is not Existing: <b>" + filename[1:] + "</b><br><br>"
            "Please try another file</center>")

    response = ("HTTP/1.1 404 Not Found\r\n"
                "Date: " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M IST")) + "\r\n"
                "Server: ChanikyaServer/0.1\r\n"
                "Content-Length: " + str(len(html)) + "\r\n"
                "Content-Type: text/html\r\n"
                "Connection: Closed\r\n\r\n")
    if isGetRequest:
        return (response + html)
    else:
        return response

# Form the HTTP homepage response to be sent to the client
def HomePageResponse():
    html = ("Welcome to Chanikya Server")
    response = ("HTTP/1.1 200 OK\r\n"
                "Date: " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M IST")) + "\r\n"
                "Server: ChanikyaServer/0.1\r\n"
                "Content-Length: " + str(html) + "\r\n"
                "Content-Type: text/html\r\n"
                "Connection: Closed\r\n\r\n")

    return (response + html)

def handleNewConnection(connectionname, connectionSocket):
    request = connectionSocket.recv(BYTES_TO_RECEIVE)
    if not request:
        return    # Basically to optimize the server I continued when no request in buffer
    print "Entered in function of" + " " + connectionname
    
    # Get the request type and file
    try:
        requestType = request.split()[0]
        requestedFile = request.split()[1]
        # Only handle GET and HEAD request types
        if requestType != 'GET' and requestType != 'HEAD':
            raise Exception;
        print("\nIncoming request:\n\n" + request)
               
    except:
        print("Malformed HTTP request; ignoring..") #Security so that none can hack the server only valid HTTP request will be served.
        return
    # Server Home page on root request. This page is hard coded in code.
    if requestedFile == "/":
        connectionSocket.send(HomePageResponse())
        return
    
    print("Requested file: " + requestedFile[1:])

    try:
        webPage = open(os.path.join(SCRIPT_LOCATION, requestedFile[1:]), 'r+')
        print(" FOUND AT " + SCRIPT_LOCATION)
        if requestType == 'GET':
            webPageSize = os.path.getsize(os.path.join(SCRIPT_LOCATION, requestedFile[1:]))
            connectionSocket.send(webPageResponse(webPageSize, requestedFile[1:]))
            for block in iter(lambda: webPage.read(BYTES_TO_RECEIVE), ""):
                connectionSocket.send(block)

            print("Finished sending " + str(webPageSize) + "/" + str(webPageSize) + " bytes to client")
        else:
            connectionSocket.send(formHeaderResponse())
        webPage.close()
    except IOError:
        # Send 404 response on not found of requested file.
        print("NOT FOUND at " + SCRIPT_LOCATION)
        connectionSocket.send(serve404Response(requestedFile, requestType == 'GET'))
    finally:
        connectionSocket.close()

def main():
    connectionList = []     #List of Parellel Connection

    # Create a TCP Socket and bind it to port (Because this is web server not client)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', SERVER_PORT))
    serverSocket.listen(10)

    print("Server is Ready and Serving the Request")

    # Infinite loop to check the request from client
    try:
        while True:
            connectionSocket, addr = serverSocket.accept()
            name = "Connection-" + str(len(connectionList))
            newconnection = myThread(len(connectionList), name, connectionSocket)
            newconnection.start()
            connectionList.append(newconnection)
            for thread in connectionList:
                if not thread.isAlive():
                    connectionList.remove( thread )
                    thread.join()
    except KeyboardInterrupt:
        print("\n^C To Stop the Server")
    finally:
        print("Server socket closed")
        serverSocket.close()

if __name__ == "__main__":
    main()
