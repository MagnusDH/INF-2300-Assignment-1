#!/usr/bin/env python3
from multiprocessing.sharedctypes import Value
import re
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
        # request_line = self.rfile.readline()

        #Dictionary containing all parts of sent-request
        request_dict = {}

        while(True):
            #Read the current line (this will iterate through all lines in request)
            byte_line = self.rfile.readline()
            
            #Decode from byte to string
            string_line = byte_line.decode()
            print("STRING LINE::::::::", string_line)

            #Make string to lowercase
            string_line = string_line.lower()

            #Place status-line, headers and body in dictionary
            if(string_line.startswith("get")):
                print("FOUND METHOD!!!!!!!!!!!!!!!!!!!!")
                print(string_line)
                request_dict = {"method": "get"}




            if(string_line.startswith("content-length:")):
                value = string_line[15:]
                value = int(value)
                request_dict = {"content-length": value}

            if(string_line.startswith("content-type:")):
                content_type = string_line[14:]
                request_dict = {"content-type": content_type}


                # hente ut Value
            if(byte_line == b"\r\n"):
                # body = self.rfile.read(content_length)
                break
                
        
        print("OOOOOOOOOOOOOOOOOOOOOOOKKKKKKKKKKKKKKKKKK")

        # i = 0
        # body = 0
        # for line in self.rfile:
        #     obj = line.decode() # Decodes from byte to string 
        #     if obj.startswith("Content-Length"):
        #         content_len = line.split(":",1)
        #         print(content_len)
        #     if(line == b"\r\n"):
        #         body = self.rfile.read(int(content_len)).decode()
        #         print(body)
        #         break
        
        # print("\n\n")
        



        # request = self.request.recv(2048)
        # # print("MAIN REQUEST:\n", request)
        # request = request.split()

        # request_parts = []

        # for line in request:
        #     line = str(line)
        #     print(line)
        #     line = line[2:]
        #     line = line.rstrip(line[-1])    #Remove last character from line
        #     request_parts.append(line)

        # print(request_parts, "\n")
        # print("Request line is:", request_line)
        
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
                #Fetch body to write to file
                # full_request = self.request.recv(1024)
                # full_request = full_request.decode()
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
    content_length = int
    content_type = string
    body = opened and read file
    """
    def WriteHeader(self, status_code, content_length, content_type, body):
        #Write status line
        if(status_code == 200):
            self.wfile.write(b"HTTP/1.1 200 - OK\r\n")
        if(status_code == 201):
            self.wfile.write(b"HTTP/1.1 201 - Created\r\n")
        if(status_code == 404):
            self.wfile.write(b"HTTP/1.1 404 - Not Found\r\n")
        if(status_code == 403):
            self.wfile.write(b"HTTP/1.1 403 - Forbidden\r\n")
        
        #Write Content-Length
        content = bytes(str(len(body)),encoding="utf-8")
        self.wfile.write(b"Content-Length: " + content)
        self.wfile.write(b"\r\n")

        #Write Content-type
        self.wfile.write(b"Content-Type: " + content_type + b"\r\n")

        #Close connection
        self.wfile.write(b"Connection: Close\r\n")

        #Write blank line before entity body
        self.wfile.write(b"\r\n")

        #Write entity body
        self.wfile.write(bytes(body))


    """
    GET-function
    file_name = which file is requested
    """
    def GET(self, file_name):  
        #If "/messages" is requested, return list/json-file
        if(file_name == "/messages"):
            file = open("messages.json", "rb")
            body = file.read()
            content_length = len(body)

            #Write status line, headers and body
            self.WriteHeader(200, content_length, b"text.json", body)
            return 1

        #Else, requested file DOES exists
        elif(self.DoesFileExist(file_name) == True):

            #If user is allowed to access given file
            if(file_name != "server.py"): 
                #If content is empty, return index.html
                if(file_name == "/"):
                    #Open and read file
                    file = open("index.html", "rb")
                    body = file.read()

                    #Write header
                    self.WriteHeader(200, len(body), b"text/html", body)

                    #Close file
                    file.close()
                    return 1
                
                else:
                    #Open and read file
                    file = open(file_name, "rb")
                    body = file.read()

                    #Write header
                    self.WriteHeader(200, str(len(body)), "text/html", body)        #Which file_type is it????????

                    #Close file
                    file.close()

                    return 1
            
            #If user is NOT allowed to open file
            else:       #This line can be written better. NOT just checking for server.py....
                self.wfile.write(b"HTTP/1.1 403 - Forbidden")
                return 0

        #File does NOT exist
        elif(self.DoesFileExist(file_name) == False):
            self.wfile.write(b"HTTP/1.1 404 - Not Found")
            return 0
        
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















































































# class MyTCPHandler(socketserver.StreamRequestHandler):    
#     """
#     This class is responsible for handling a request. The whole class is
#     handed over as a parameter to the server instance so that it is capable
#     of processing request. The server will use the handle-method to do this.
#     It is instantiated once for each request!
#     Since it inherits from the StreamRequestHandler class, it has two very
#     usefull attributes you can use:

#     rfile - This is the whole content of the request, displayed as a python
#     file-like object. This means we can do readline(), readlines() on it!

#     wfile - This is a file-like object which represents the response. We can
#     write to it with write(). When we do wfile.close(), the response is
#     automatically sent.

#     The class has three important methods:
#     handle() - is called to handle each request.
#     setup() - Does nothing by default, but can be used to do any initial
#     tasks before handling a request. Is automatically called before handle().
#     finish() - Does nothing by default, but is called after handle() to do any
#     necessary clean up after a request is handled.
#     """
#     def handle(self):
#         """
#         This method is responsible for handling an http-request. You can, and should(!),
#         make additional methods to organize the flow with which a request is handled by
#         this method. But it all starts here!
#         """

#         #Read the request
#         full_request_line = self.request.recv(1024)
#         full_request_line = full_request_line.decode()

#         #Parse the request into a dictionary
#         request_dict = self.parse_request(full_request_line)


#     #     #Read the request
#     #     request_line = self.rfile.readline()


#     #         #Parse the request
#     #         request_parts = self.parse_request(full_request_line)

#     #     #Read the request
#     #     request_line = self.rfile.readline()
        
#     #     #Parse the request
#     #     request_parts = self.parse_request(request_line)

#     #     #Check for directory traversal attack
#     #     TraversalAttackString = "../"
#     #     if(TraversalAttackString in request_parts[1]):
#     #         self.wfile.write(b"HTTP/1.1 403 - Forbidden")

#     #     #Request is not a directory traversal attack
#     #     else:
#     #         #Handle the request
#     #         if(request_parts[0]) == "GET":
#     #             request_content = self.GET(request_parts[1])

#     #         elif(request_parts[0]) == "POST":
#     #             self.POST(request_parts[1])

#     #         #Request method is not recognized
#     #         else:
#     #             print("ERROR: Could not parse request line")


#     """
#     Parses a request line into a dictionary.
#     Key = headers
#     Value = content in header

#     (Keys: Method, FileName, Version, Host, Accept-Encoding)
#     """
#     def parse_request(self, full_request):
#         #Create dictionary
#         dictionary = {}
        
#         print("\nFULL REQUEST:\n", full_request)
        
#         #Parse lines from full_request into list
#         request_lines = full_request.split("\r\n")
#         print("Printing list:\n", request_lines, "\n")

#         request_parts = []
#         for x in request_lines:
#             request_parts.append(x.split(" "))

#         print(request_parts[0][0])
        
#         #Add parts to dictionary
#         dictionary = {
#             "Method": request_parts[0][0],
#             "FilePath": request_parts[0][1],
#             ""
#             }

#         # request_words = re.split("\n", full_request)
#         # print(request_words)
#         # request_words = request_parts[0].decode("utf-8").split()
#         # print("Request words:", request_words)

#         # print("Request words list:", request_words, "\n")

#         return dictionary

    # """
    # Returns TRUE if the file exists
    # Return FALSE if the file does NOT exist
    # """
    # def DoesFileExist(self, FilePathName):
    #     return os.path.exists(FilePathName)

    # """
    # status_code = int
    # content_length = string
    # content_type = string
    # body = opened and read file
    # """
    # def WriteHeader(self, status_code, content_length, content_type, body):
    #     #Write status line
    #     if(status_code == 200):
    #         self.wfile.write(b"HTTP/1.1 200 - OK\r\n")
    #     if(status_code == 404):
    #         self.wfile.write(b"HTTP/1.1 404 - Not Found")
    #     if(status_code == 403):
    #         self.wfile.write(b"HTTP/1.1 403 - Forbidden")
        
    #     # else:
    #         # print("STATUS CODE NOT ACCEPTED in WriteHeader function")

    #     #Write Content-Length
    #     string = "Content-Length: " + content_length
    #     self.wfile.write(b"Content-Length: ")
    #     self.wfile.write(b"\r\n")
    #     self.wfile.write(bytes(string, encoding="utf-8"))
    #     self.wfile.write(b"\r\n")

    #     #Write Content-type
    #     self.wfile.write(b"Content-Type: text/html\r\n")


    #     #Write blank line before entity body
    #     self.wfile.write(b"\r\n")

    #     #Write entity body
    #     self.wfile.write(bytes(body))


    # """
    # GET-function
    # file_name = which file is requested
    # """
    # def GET(self, file_name):     
    #     #If requested file exists
    #     if(self.DoesFileExist(file_name) == True):

    #         #If user is allowed to access given file
    #         if(file_name != "server.py"): 
    #             #If content is empty, return index.html
    #             if(file_name == "/"):
    #                 #Open and read file
    #                 file = open("index.html", "rb")
    #                 body = file.read()

    #                 #Write header
    #                 self.WriteHeader(200, str(len(body)), "text/html", body)

    #                 #Close file
    #                 file.close()
                
    #             else:
    #                 #Open and read file
    #                 file = open(file_name, "rb")
    #                 body = file.read()

    #                 #Write header
    #                 self.WriteHeader(200, str(len(body)), "text/html", body)        #Which file_type is it????????

    #                 #Close file
    #                 file.close()
            
    #         #If user is NOT allowed to open file
    #         else:       #This line can be written better. NOT just checking for server.py....
    #             self.wfile.write(b"HTTP/1.1 403 - Forbidden")

    #     #File does NOT exist
    #     elif(self.DoesFileExist(file_name) == False):
    #         self.wfile.write(b"HTTP/1.1 404 - Not Found")
        
    #     # A GET request to a resource that does not exist should return a 404 - Not Found status with an optional HTML body.
    #     # A GET request to a forbidden resource such as server.py should return a 403 - Forbidden status with an optional HTML body.
    #     # Any successful GET request should return a 200 - Ok response code and the requested resource.
    #     # Any request or response with a non-empty body MUST contain the 'Content-Length' header. This field is simply the exact size of the body in bytes.


    # """
    # Creates a new file with the given "file_name".
    # Appends the "content" to the new file
    # """
    # def POST(self, file_name):
    #     #If file already exists
    #     if(self.DoesFileExist(file_name) == True):
    #         self.wfile.write(b"HTTP/1.1 406 - Not Acceptable")
        
    #     #File does not exist, create new one
    #     elif(self.DoesFileExist(file_name) == False):
    #         new_file = open(file_name, "a")
    #         #Write content to new file
    #         new_file.close()
    #         self.wfile.write(b"HTTP/1.1 201 - Created")



        # A POST request to /test.txt should create the resource if it does not exist. The content of the request body should be appended to the file, and its complete contents should be returned in the response body.
        # A POST request to any other file should return a 403 - Forbidden with an optional HTML body.
        # Any request or response with a non-empty body MUST contain the 'Content-Length' header. This field is simply the exact size of the body in bytes.



# if __name__ == "__main__":
#     HOST, PORT = "localhost", 8080
#     socketserver.TCPServer.allow_reuse_address = True
#     with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
#         print("Serving at: http://{}:{}".format(HOST, PORT))
#         server.serve_forever()