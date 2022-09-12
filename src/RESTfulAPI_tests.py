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
    #Write request message to server.py    
    client.request("GET", "/messages")

    expected_answer = "b'test string'"
    
    response = client.getresponse().read()

    answer2 = str(response).split("\n")

    print("\nResponse is:", answer2)

    if(expected_answer == str(response)):
        client.close()
        return True
    else:
        client.close()
        return False
    
    
test_functions = [
    test_GET_messages,
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