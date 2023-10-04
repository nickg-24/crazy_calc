import sys
import re
import socket
import ssl
import threading
import parser_1 # for the parser function

methods = ["GET", "POST", "PUT", "DELETE"]
httpVersions = ["HTTP/1.1", "HTTP/1.0"]
schemes = ["http", "https"]

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    # checks if the resquest is sytactically valid
    req_syntax_code = parser_1.validate(request)

    print('Response would be:',req_syntax_code)

    # if parser code was 200, proceed
    if req_syntax_code[0] == 200:
        # now handle method specific actions
        # get required info from the parser
        method = req_syntax_code[1]
        uri = req_syntax_code[2]

        if method == "GET":
            print("do get stuff")
        elif method == "POST":
            print("do post stuff")
        elif method == "PUT":
            print("do put stuff")
        elif method == "DELETE":
            print ("do delete stuff")
        else:
            print("we have a problem, this should never print. I missed a case in the parser")

    # otherwise do error logic
    else:
        print(req_syntax_code)


    # send data back to client and close connection
    client_socket.send("connection closing".encode())
    client_socket.close()

    
# handles get requests
def get_req():
    print("foo")

# handles post requests
def post_req():
    print("foo")

# handles put requests
def put_req():
    print("foo")

def delete_req():
    print("foo")


    

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