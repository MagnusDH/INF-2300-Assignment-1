from multiprocessing.connection import answer_challenge
import socketserver
import threading
from server import MyTCPHandler as HTTPHandler
from http import HTTPStatus
from http.client import HTTPConnection, BadStatusLine
import os
from random import shuffle

HOST = "localhost"
PORT = 54321

class MockServer(socketserver.TCPServer):
    allow_reuse_address = True


server = MockServer((HOST, PORT), HTTPHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()
client = HTTPConnection(HOST, PORT)

def test_GET_messages():
    """
    Checks if messages.json response is correct
    """
    #Write request message to server.py    
    client.request("GET", "/messages")

    #Open file and save the expected response
    file = open("messages.json", "rb")
    expected_response = file.read()
    
    #Read the actual response from server
    response = client.getresponse().read()

    #Check responses
    if(expected_response == response):
        client.close()
        return True
    else:
        client.close()
        return False

def test_POST_to_messages():
    """
    Checks if POST to "/messages" is correct
    """
    #Write request message
    file_name = "magnus.json"
    content = "Magnus e sykt kul"
    headers = {
        "content-type": "text.json",
        "content-length": len(content)
    }

    #Remove test file if it exists
    if(os.path.exists(file_name) == True):
        os.remove(file_name)

    client.request("POST", file_name, body=content, headers=headers)
    print("Expected response:", content)

    #Check response
    response = client.getresponse().read()
    print("Actual response:", response)

    if(response == content):
        client.close()
        return 1
    else:
        client.close()
        return 0


    
test_functions = [
    # test_GET_messages,
    test_POST_to_messages
]


def run_tests(all_tests, random=False):
    print("Running tests in sequential order...\n")
    passed = 0
    failed = 0
    num_tests = len(all_tests)

    #Run all tests
    for test_function in all_tests:
        result = test_function()
        
        if(result == True):
            passed += 1
        else:
            failed += 1
    
    percent = round((passed / num_tests) * 100, 2)
    
    print("PASSED", passed, "/", num_tests, "TESTS", "(", percent, "%)")


run_tests(test_functions)
server.shutdown()