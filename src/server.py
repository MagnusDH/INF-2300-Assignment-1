#!/usr/bin/env python3
import socketserver
from urllib import request


"""
Written by: Raymon Skjørten Hansen
Email: raymon.s.hansen@uit.no
Course: INF-2300 - Networking
UiT - The Arctic University of Norway
May 9th, 2019
"""



class MyTCPHandler(socketserver.StreamRequestHandler):    
    """
    This class is responsible for handling a request. The whole class is
    handed over as a parameter to the server instance so that it is capable
    of processing request. The server will use the handle-method to do this.
    It is instantiated once for each request!
    Since it inherits from the StreamRequestHandler class, it has two very
    usefull attributes you can use:

    rfile - This is the whole content of the request, displayed as a python
    file-like object. This means we can do readline(), readlines() on it!

    wfile - This is a file-like object which represents the response. We can
    write to it with write(). When we do wfile.close(), the response is
    automatically sent.

    The class has three important methods:
    handle() - is called to handle each request.
    setup() - Does nothing by default, but can be used to do any initial
    tasks before handling a request. Is automatically called before handle().
    finish() - Does nothing by default, but is called after handle() to do any
    necessary clean up after a request is handled.
    """
    def handle(self):
        """
        This method is responsible for handling an http-request. You can, and should(!),
        make additional methods to organize the flow with which a request is handled by
        this method. But it all starts here!
        """

        #Read the request
        request_line = self.rfile.readline()
        print("Reading request:", request_line)
        
        #Parse the request
        print("Parsing request...")
        request_parts = self.parse_request(request_line)
        
        #Handle the request
        print("Handling request...")
        if(request_parts[0]) == "GET":
            request_content = self.GET(request_parts[1])

        # if(request_parts[0]) == "POST":
        #     POST()
        else:
            print("ERROR: Could not parse request line")
        


    """
    Parses a request line.
    The words in the line is returned as a list.
    list[0] = request method
    list[0] = content to fetch
    list[0] = HTTP version
    list[0] = \r
    list[0] = \n
    """
    def parse_request(self, request_line):
    
        request_words = request_line.decode("utf-8").split()
        return request_words

    """
    GET-function
    Content = what to fetch
    """
    def GET(self, content):
        print("\nGET function...\n")

        #If content is empty, return index.html
        if(content == "/"):
            try:
                file = open("index.html", "rb")
                body = file.read()

                #Write status line
                self.wfile.write(b"HTTP/1.1 200 OK\r\n")

                #Write header lines
                self.wfile.write(b"Content-Length: ", len(body), "\r\n")
                # self.wfile.write(b"Content-Type: ", "html\r\n")
                #Content type
                #Connection: closed

                #Write empty spaces
                self.wfile.write(b"\r\n")

                #Write entity body
                self.wfile.write(bytes(body))
                
                #Close file
                file.close()

            #File does not exist, write HTTP error message
            except:
                self.wfile.write(b"HTTP/1.1 404 - Not Found")



        # To do:
            # Find out what to get (a text.txt file maybe)
            # Return tekst.txt file
            # Respond with status code (200 OK, NOt OK etc ...)
            

        # A GET request to a resource that does not exist should return a 404 - Not Found status with an optional HTML body.
        # A GET request to a forbidden resource such as server.py should return a 403 - Forbidden status with an optional HTML body.
        # Any successful GET request should return a 200 - Ok response code and the requested resource.
        # Any request or response with a non-empty body MUST contain the 'Content-Length' header. This field is simply the exact size of the body in bytes.


def POST():
    print("\nPOST function...\n")

    # A POST request to /test.txt should create the resource if it does not exist. The content of the request body should be appended to the file, and its complete contents should be returned in the response body.
    # A POST request to any other file should return a 403 - Forbidden with an optional HTML body.
    # Any request or response with a non-empty body MUST contain the 'Content-Length' header. This field is simply the exact size of the body in bytes.


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("Serving at: http://{}:{}".format(HOST, PORT))
        server.serve_forever()
