#!/usr/bin/env python3
import socketserver
from urllib import request
import os


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
        
        #Parse the request
        request_parts = self.parse_request(request_line)

        #Check for directory traversal attack
        TraversalAttackString = "../"
        if(TraversalAttackString in request_parts[1]):
            self.wfile.write(b"HTTP/1.1 403 - Forbidden")

        #Request is not a directory traversal attack
        else:
            #Handle the request
            if(request_parts[0]) == "GET":
                request_content = self.GET(request_parts[1])

            elif(request_parts[0]) == "POST":
                self.POST(request_parts[1])

            #Request method is not recognized
            else:
                print("ERROR: Could not parse request line")


    """
    Parses a request line.
    The words in the line is returned as a list.
    list[0] = request method
    list[1] = content to fetch
    list[2] = HTTP version
    list[3] = \r
    list[4] = \n
    """
    def parse_request(self, request_line):
    
        request_words = request_line.decode("utf-8").split()
        return request_words


    """
    Returns TRUE if the file exists
    Return FALSE if the file does NOT exist
    """
    def DoesFileExist(self, FilePathName):
        return os.path.exists(FilePathName)

    """
    status_code = int
    content_length = string
    content_type = string
    body = opened and read file
    """
    def WriteHeader(self, status_code, content_length, content_type, body):
        #Write status line
        if(status_code == 200):
            self.wfile.write(b"HTTP/1.1 200 - OK\r\n")
        if(status_code == 404):
            self.wfile.write(b"HTTP/1.1 404 - Not Found")
        if(status_code == 403):
            self.wfile.write(b"HTTP/1.1 403 - Forbidden")
        
        # else:
            # print("STATUS CODE NOT ACCEPTED in WriteHeader function")

        #Write Content-Length
        string = "Content-Length: " + content_length
        self.wfile.write(b"Content-Length: ")
        self.wfile.write(b"\r\n")
        self.wfile.write(bytes(string, encoding="utf-8"))
        self.wfile.write(b"\r\n")

        #Write Content-type
        self.wfile.write(b"Content-Type: text/html\r\n")


        #Write blank line before entity body
        self.wfile.write(b"\r\n")

        #Write entity body
        self.wfile.write(bytes(body))


    """
    GET-function
    file_name = which file is requested
    """
    def GET(self, file_name):     
        #If requested file exists
        if(self.DoesFileExist(file_name) == True):

            #If user is allowed to access given file
            if(file_name != "server.py"): 
                #If content is empty, return index.html
                if(file_name == "/"):
                    #Open and read file
                    file = open("index.html", "rb")
                    body = file.read()

                    #Write header
                    self.WriteHeader(200, str(len(body)), "text/html", body)

                    #Close file
                    file.close()
                
                else:
                    #Open and read file
                    file = open(file_name, "rb")
                    body = file.read()

                    #Write header
                    self.WriteHeader(200, str(len(body)), "text/html", body)        #Which file_type is it????????

                    #Close file
                    file.close()
            
            #If user is NOT allowed to open file
            else:       #This line can be written better. NOT just checking for server.py....
                self.wfile.write(b"HTTP/1.1 403 - Forbidden")

        #File does NOT exist
        elif(self.DoesFileExist(file_name) == False):
            self.wfile.write(b"HTTP/1.1 404 - Not Found")
        
        # A GET request to a resource that does not exist should return a 404 - Not Found status with an optional HTML body.
        # A GET request to a forbidden resource such as server.py should return a 403 - Forbidden status with an optional HTML body.
        # Any successful GET request should return a 200 - Ok response code and the requested resource.
        # Any request or response with a non-empty body MUST contain the 'Content-Length' header. This field is simply the exact size of the body in bytes.


    """
    Creates a new file with the given "file_name".
    Appends the "content" to the new file
    """
    def POST(self, file_name):
        #If file already exists
        if(self.DoesFileExist(file_name) == True):
            self.wfile.write(b"HTTP/1.1 406 - Not Acceptable")
        
        #File does not exist, create new one
        elif(self.DoesFileExist(file_name) == False):
            new_file = open(file_name, "a")
            #Write content to new file
            new_file.close()
            self.wfile.write(b"HTTP/1.1 201 - Created")



        # A POST request to /test.txt should create the resource if it does not exist. The content of the request body should be appended to the file, and its complete contents should be returned in the response body.
        # A POST request to any other file should return a 403 - Forbidden with an optional HTML body.
        # Any request or response with a non-empty body MUST contain the 'Content-Length' header. This field is simply the exact size of the body in bytes.



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("Serving at: http://{}:{}".format(HOST, PORT))
        server.serve_forever()
