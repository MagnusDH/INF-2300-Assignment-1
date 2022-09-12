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
    

    try:
        response = client.getresponse()
        return response.status in [status.value for status in HTTPStatus]
    except BadStatusLine:
        client.close()
        return False

def test_POST_new_message():
    testfile = "tekst.txt"
    msg = b"Denne teksten skal inn i tekst.txt"
    
    headers = {
        "Content-Type:": "txt",
        "Content-Length:": bytes(len(msg))
    }

    if(os.path.exists(testfile)):
        print("File already exists on server...")
        return False
    else:
        client.request("POST", testfile, body=msg, headers=headers)
        client.getresponse()
        client.close()
        return True

    
test_functions = [
    test_GET_messages,
    # test_POST_new_message,
]


def run_tests(all_tests, random=False):
    print("Running tests in sequential order...\n")
    passed = 0
    num_tests = len(all_tests)
    skip_rest = False
    for test_function in all_tests:
        if not skip_rest:
            result = test_function()
            if result:
                passed += 1
            else:
                skip_rest = True
            print(("FAIL", "PASS")[result] + "\t" + test_function.__doc__)
        else:
            print("SKIP\t" + test_function.__doc__)
    percent = round((passed / num_tests) * 100, 2)
    print(f"\n{passed} of {num_tests}({percent}%) tests PASSED.\n")
    if passed == num_tests:
        return True
    else:
        return False


run_tests(test_functions)
server.shutdown()