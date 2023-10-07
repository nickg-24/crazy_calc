import sys
import re
import socket
import ssl
import threading
import parser_1 # for the parser function
import os
import subprocess
import datetime

methods = ["GET", "POST", "PUT", "DELETE"]
httpVersions = ["HTTP/1.1", "HTTP/1.0"]
schemes = ["http", "https"]
DOCUMENT_ROOT = "../www"
LOG_FILE = "../logs/valid_requests.log"

# recieves request and sends response to client
def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    # checks if the resquest is sytactically valid
    print(request)
    req_syntax_code = parser_1.validate(request)

    # print('Response would be:',req_syntax_code) # for testing

    # if parser code was 200 and its a tuple, proceed
    if isinstance(req_syntax_code, tuple) and req_syntax_code[0] == 200:
        # log the first line of the valid request
        top_line = request.split('\r\n')[0]
        date_and_time = datetime.datetime.now()
        subprocess.call(f'echo {date_and_time} : {top_line} >> {LOG_FILE}', shell=True) # possible RCE vulnerability

        # now handle method specific actions
        # get required info from the parser
        method = req_syntax_code[1]
        uri = req_syntax_code[2]

        if method == "GET":
            content, status_code = get_req(uri)
            response = format_response(status_code, content)
        elif method == "POST":
            print("do post stuff")
        elif method == "PUT":
            print("do put stuff")
        elif method == "DELETE":
            content, status_code = delete_req(uri)
            response = format_response(status_code, content)
        else:
            print("we have a problem, this should never print. I missed a case in the parser")

    # otherwise, format the response using the code from the parser
    else:
        response = format_response(req_syntax_code[0])


    # send data back to client and close connection
    client_socket.send(response.encode())
    client_socket.close()

# given a file path, returns the contents of the file
def file_read(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    

    
# handles get requests, returns a tuple (response, status code)
def get_req(uri):
    # handle document route
    sys_path = DOCUMENT_ROOT + uri

    # check if file exists
    if os.path.isfile(sys_path):
        #print(f'{sys_path} exists') # for testing
        # need to add a check to see if has permissions to access file
        # return file contents and status code
        return file_read(sys_path), 200
    else:
        # return 404 file not found
        #print(f'{sys_path} does not exist') # for testing
        return "", 404


# handles post requests, returns a tuple (response, status code)
def post_req(uri, body):
    # 
    print("foo")

# handles put requests, returns a tuple (response, status code)
# create file at uri, contents of body. will overwrite existing files
def put_req(uri, body):
    print("foo")
    #

# deletes a resource, returns a tuple (response, status code)
def delete_req(uri):
    sys_path = DOCUMENT_ROOT + uri
    # check if the file exists
    if os.path.isfile(sys_path):
       #delete it
       os.remove(sys_path)
       return "", 200
    else:
        # return 404 file not found
        #print(f'{sys_path} does not exist') # for testing
        return "", 404

    # if it does not e

#takes outputs of method and nicely formats it to send back to client
def format_response(status_code, content=""):
    responses = {
        200: ("OK", content),
        201: ("Created", content),
        400: ("Bad Request", "<h1>400 Error: Bad Request</h1>"),
        403: ("Forbidden", "<h1>403 Error: Forbidden</h1>"),
        404: ("Not Found", "<h1>404 Error: Resource Not Found</h1>"),
        411: ("Length Required", "<h1>411 Error: Length Required</h1>"),
        500: ("Internal Server Error", "<h1> 500 Error: Internal Server Error</h1>"),
        501: ("Not Implemented", "<h1>501 Error: Method Not Implemented</h1>"),
        505: ("HTTP Version Not Supported", "<h1>505 Error: HTTP Version Not Supported</h1>")
    }

    response_message, response_body = responses[status_code]
    response = f"HTTP/1.1 {status_code} {response_message}\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
    return response


def main():
    ip_addr = sys.argv[1]
    port = int(sys.argv[2])

    print(f'{ip_addr}:{port}') # debug comment

    # if there are 5 args, then all args have been provided
    is_https = len(sys.argv) == 5

    # if cert and key are present, it is https
    if is_https:
        cert_path = sys.argv[3]
        pk_path = sys.argv[4]
        print(f'\n {cert_path} \n {pk_path}') # debug comment
    print("is https=" , is_https) # debug comment


    # if its not https, open standard socket
    if not is_https:
        # listen on specified ip and port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip_addr, port))
        s.listen(5)
        while True:
            client, address = s.accept()
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()

    # if it is https, open https socket
    if is_https:
        print('do the same thing but will ssl')
        print('work in progress')
main()