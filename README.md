# INF-2300-Assignment-1


In this assignment, you will learn about the HyperText Transfer Protocol (HTTP): one of the most popular and versatile protocols on the Internet. An HTTP web server provides one or more network endpoints that clients can connect to using TCP and issue HTTP formatted requests. The server can respond by sending data from a file, a database, or simply a confirmation of some task being completed.

To complete this assignment, you must implement an HTTP server that exposes several endpoints: some for web browsers and some for RESTul API clients.

Your HTTP endpoints must be made available to the TAs from your private course server.

Specifications
Browser endpoints
The following endpoints are used by web browsers.

HTTP methods 	URI	Action
GET	/	Return index.html in the body of the response.
GET	/index.html	Return index.html in the body of the response.
POST	/test.txt	Write body to test.txt file.
Your server should respond with the correct HTTP response code.

A GET request to a resource that does not exist should return a 404 - Not Found status with an optional HTML body.
A GET request to a forbidden resource such as server.py should return a 403 - Forbidden status with an optional HTML body.
Any successful GET request should return a 200 - Ok response code and the requested resource.
A POST request to /test.txt should create the resource if it does not exist. The content of the request body should be appended to the file, and its complete contents should be returned in the response body.
A POST request to any other file should return a 403 - Forbidden with an optional HTML body.
Any request or response with a non-empty body MUST contain the 'Content-Length' header. This field is simply the exact size of the body in bytes.

RESTful API endpoints
The second set of endpoints exposes a simple message service where a RESTful client can Create, Update, and Delete (CRUD) JSON-formatted messages.

An important requirement of this assignment is that messages are not lost due to server failures or restarts. For this, you must implement a mechanism that persists the state to stable storage, like a disk or a database.

It is important to understand that the /messages endpoint differs from the previous ones in it represents a resource or service and not simply files on disk.

The following API must be implemented.

HTTP methods 	URI	Action
GET	/messages	Return all stored messages.
POST	/messages	Create a new message.
PUT	/messages	Update message.
DELETE	/messages	Delete message.
A message object should contain two fields: text and id.

{
"id": 1,
"text": "Example text"
}
GET /messages
A GET request to /messages should return a JSON-formatted list of all messages currently stored.

[{
"id": 1,
"text": "Example text"
},
{
"id": 2,
"text": "More example text"
}]
POST /messages
A POST request to /messages should accept a JSON-formatted entity-body. It should persist the message so it can be retrieved later. The response should be 201 - Created and a body containing the newly created message object. Example: Request:

{"text": "Example text"}
Response:

{
"id": 3,
"text": "Example text"
}
PUT /messages
A PUT request to /messages should accept a JSON-formatted entity-body with an id and text field. The server should find the message with the corresponding id and replace the text field with the one from the request.

DELETE /messages
A DELETE request to /messages should accept a JSON-formatted entity-body, find the message with the corresponding id and remove the message. The response should be 200 - Ok.

Precode
To get you started, we have made available a template precode  Last ned precode.

server.py is an empty socket-server handler in Python. Simply run this script to start the server. The handler method process incoming requests. See the precode comments and Python documentation for more information. The server binds to port 8080.
client.py is a simple test client to run against your HTTP server solution. It assumes your server is in server.py. The client makes a series of requests and checks the responses. If you are unsure where to begin, the test client is written to function as a guide to help you get started. The test client is not meant to be a complete requirements test, nor does it present the only way to solve the assignment.
Special cases
The specifications presented here are incomplete. This is deliberate. There is no commonly agreed-upon set of specifications for a RESTful Web API. This is because they are very use-case dependent. For the edge cases, make choices that seem logical. Be consistent. Explain your choices in the report. Here are some examples of edge cases (there are many more!) to consider:

Non-supported request methods like HEAD, DELETE, or PIZZA, for that matter, shouldn't crash the server.
POST request to server.py?
Non-supported request methods like HEAD, DELETE, or PIZZA shouldn't crash the server.
DELETE request to a non-existent message?
GET request to empty resource?
POST request with id field? POST request with NO text field?
Empty POST, PUT and DELETE requests?
PUT request with no id? 201 or 404?
PUT request with an existing id but no text field?
Requirements
Your server must implement the specification above and be available to the TAs on the public Internet. To summarize:

Static HTTP-server running on your curse server (e.g., hjo001.csano.no)
supporting basic GET and POST requests
RESTful Web API server running on your course server
supporting GET, POST, PUT, and DELETE to /messages using JSON-formatted body.
The /messages resource should persist between runs.
Responses should contain the Content-Length and Content-Type headers as a minimum.
Ideally, both services are supported by the same server process.

You may use libraries such as JSON and urlllib, but none that trivialities the assignment, such as httpserver or similar. If you are unsure, ask your TA.

Tips
Write encourage you to write a single server for all HTTP endpoints. If you implement two servers: one static HTTP and one RESTful API, you will end up copying & pasting a lot of code. A good solution will have generic code usable in both parts of the assignment.

When parsing requests, do not assume anything about the configuration of the headers. There might be only one, or there might be 20. Test your code with different browsers and different numbers of headers, body lengths, etc.

Send manual requests to existing servers, and check the responses.

Extra credit
Consider security holes in your solution. Path traversal attacks? Whitelist rather than a blacklist.
Implement redirecting from / to /index.html
Implement Server and Date headers.
Implement another level in the /messages resource such that: GET, PUT and DELETE requests to
/messages/<id> is resolved to the id in the URL and not the JSON object in the body. This is how most
RESTful APIs do it.
Resources
For all available HTTP-response codes:
https://http.cat/ (Lenker til en ekstern side.)
For manually sending requests from the command line, use httpie. Multi-platform support. Easy to use. This will save you a lot of time!
https://httpie.org/ (Lenker til en ekstern side.)
A wealth of information on RESTful APIs:
https://restapitutorial.com/ (Lenker til en ekstern side.)
If you prefer a GUI-based interface for testing your server. Insomnia is a good multi-platform tool.
https://insomnia.rest/ (Lenker til en ekstern side.)
Hypertext Transfer Protocol - HTTP/1.1:
https://tools.ietf.org/html/rfc2616 (Lenker til en ekstern side.)
HTTP - Message Syntax and Routing:
https://tools.ietf.org/html/rfc7230 (Lenker til en ekstern side.)
HTTP - Semantics and Content:
https://tools.ietf.org/html/rfc7231 (Lenker til en ekstern side.)
HTTP - Conditional Requests:
https://tools.ietf.org/html/rfc7232 (Lenker til en ekstern side.)
HTTP - Range Requests:
https://tools.ietf.org/html/rfc7233 (Lenker til en ekstern side.)
HTTP - Caching:
https://tools.ietf.org/html/rfc7234 (Lenker til en ekstern side.)
HTTP - Authentication:
https://tools.ietf.org/html/rfc7235 (Lenker til en ekstern side.)
Hand-In
Hand in your solution and the report by uploading it in a compressed file to Canvas. Your report should be in pdf format in the doc folder. Remember to update your README!
