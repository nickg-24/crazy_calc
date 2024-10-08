import sys
import re
import socket
import ssl
import threading
import parser_1 # for the parser function
import os
import subprocess
import datetime
import php_exec # for php functionality

methods = ["GET", "POST", "PUT", "DELETE"]
httpVersions = ["HTTP/1.1", "HTTP/1.0"]
schemes = ["http", "https"]
DOCUMENT_ROOT = "../www"
LOG_FILE = "../logs/valid_requests.log"
ERROR_LOG = "../logs/internal_errors.log"
CERT_FILE = "../ssl/certificate.pem"
KEY_FILE = "../ssl/private_key.pem"



# recieves request and sends response to client
def handle_client(client_socket):
    # try to handle the client request
    try:
        request = receive_full_request(client_socket)
        # checks if the resquest is sytactically valid
        print(request)
        req_syntax_code = parser_1.validate(request)

        # print('Response would be:',req_syntax_code) # for testing

        # if parser code was 200 and its a tuple, proceed
        if isinstance(req_syntax_code, tuple) and req_syntax_code[0] == 200:
            # log the first line of the valid request
            top_line = request.split('\r\n')[0]
            date_and_time = datetime.datetime.now()
            subprocess.call(f"echo '{date_and_time}' : '{top_line}' >> {LOG_FILE}", shell=True) # possible RCE vulnerability

            # now handle method specific actions
            # get required info from the parser
            method = req_syntax_code[1]
            uri = req_syntax_code[2]
            body = req_syntax_code[3] if len(req_syntax_code) > 3 else None


            if method == "GET":
                content, status_code = get_req(uri)
                response = format_response(status_code, content)
            elif method == "POST":
                content, status_code = post_req(uri, body)
                response = format_response(status_code, content)
            elif method == "PUT":
                content, status_code = put_req(uri, body)
                response = format_response(status_code, content, uri if status_code == 201 else None)
            elif method == "DELETE":
                status_code = delete_req(uri)
                response = format_response(status_code)
            else:
                print("we have a problem, this should never print. I missed a case in the parser")

        # otherwise, format the response using the code from the parser
        else:
            pre_response = req_syntax_code[0] if isinstance(req_syntax_code, tuple) else req_syntax_code
            response = format_response(pre_response)
    # something broke, 500 Internal Server Error
    except Exception as e:
        # log to errors file
        date_and_time = datetime.datetime.now()
        subprocess.call(f'echo {date_and_time} : {e} >> {ERROR_LOG}\r\n\r\n', shell=True) # possible RCE vulnerability
        
        response = format_response(500)
    # send data back to client and close connection
    send_full_data(client_socket, response.encode())
    client_socket.close()

# given a file path, returns the contents of the file
def file_read(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    

    
# handles get requests, returns a tuple (response, status code)
def get_req(uri):
    # separate the path from the query string
    parts = uri.split("?", 1)
    path = parts[0]
    params= parts[1] if len(parts) > 1 else None
    # print("GET PARAMS:", params)
    
    # handle document route
    sys_path = DOCUMENT_ROOT + path

    # check if file exists
    if os.path.isfile(sys_path):
        # Check if the requested file is a PHP file
        if sys_path.endswith(".php"):
            try:
                content = php_exec.execute_php("GET", sys_path, query_string=params)
                return content, 200
            except Exception as e:
                print("Error executing PHP script:", e)
                return "", 500
        else:
            return file_read(sys_path), 200
    else:
        return "", 404


# handles post requests, returns a tuple (response, status code)
def post_req(uri, body):
    # separate the path from the query string
    parts = uri.split("?", 1)
    path = parts[0]

    # handle document route
    sys_path = DOCUMENT_ROOT + path

     # check if the file exists
    if os.path.isfile(sys_path):
        # check if the requested file is a php file
        if sys_path.endswith(".php"):
            try:
                content = php_exec.execute_php("POST", sys_path, post_body=body)
                return content, 200
            except Exception as e:
                print("Error executing PHP script:", e)
                return "", 500
        else:
            content = file_read(sys_path)
            status_code = 200
            return content, status_code
    else:
        return "", 404




# handles put requests, returns a tuple (response, status code)
# create file at uri, contents of body. will overwrite existing files
def put_req(uri, body):
    sys_path = DOCUMENT_ROOT + uri
    # check if the file exists
    if os.path.isfile(sys_path):
        try:
            # overwrite the content
            with open(sys_path, 'w') as file:
                file.write(body)
            return file_read(sys_path), 200 # return content
        except:
            return "", 500
    else:
        try:
            # create new file, contains the body
            with open(sys_path, 'w') as file:
                file.write(body)
            return file_read(sys_path), 201 # return content
        except:
            return "", 500


# deletes a resource, returns a tuple (response, status code)
def delete_req(uri):
    sys_path = DOCUMENT_ROOT + uri
    # check if the file exists
    if os.path.isfile(sys_path):
       #delete it
       os.remove(sys_path)
       return 200
    else:
        # return 404 file not found
        #print(f'{sys_path} does not exist') # for testing
        return 404


#takes outputs of method and nicely formats it to send back to client
def format_response(status_code, content="", location=None):
    responses = {
        200: ("OK", content),
        201: ("Created", content),
        400: ("Bad Request", "<h1>400 Error: Bad Request</h1>"),
        403: ("Forbidden", "<h1>403 Error: Forbidden</h1>"),
        404: ("Not Found", "<h1>404 Error: Resource Not Found</h1>"),
        411: ("Length Required", "<h1>411 Error: Length Required</h1>"),
        415: ("Unsupported Media Type", "<h1>415 Error: Unsupported Media Type</h1>"),
        500: ("Internal Server Error", "<h1> 500 Error: Internal Server Error</h1>"),
        501: ("Not Implemented", "<h1>501 Error: Method Not Implemented</h1>"),
        505: ("HTTP Version Not Supported", "<h1>505 Error: HTTP Version Not Supported</h1>")
    }

    response_message, response_body = responses[status_code]
    response_headers = [
        f"HTTP/1.1 {status_code} {response_message}",
        f"Content-Length: {len(response_body)}",
        "Content-Type: text/html"
    ]

    if location:
        response_headers.append(f"Location: {location}")
    
    return "\r\n".join(response_headers) + "\r\n\r\n" + response_body

# loops to make sure full request is recieved
def receive_full_request(sock, buffer_size=1024):
    data = b""
    while True:
        part = sock.recv(buffer_size)
        data += part
        if b"\r\n\r\n" in part or not part:
            break
    return data.decode()

# loops to make sure full response is sent
def send_full_data(sock, data):
    bytes_sent = 0
    while bytes_sent < len(data):
        bytes_sent += sock.send(data[bytes_sent:])

def main():
    if len(sys.argv) < 3:
        print("Usage: server.py <ip> <http_port>")
        sys.exit(1)

    ip_addr = sys.argv[1]
    http_port = int(sys.argv[2])
    https_port = 443  # Fixed port for HTTPS

    print(f'HTTP server listening at {ip_addr}:{http_port}')
    print(f'HTTPS server listening at {ip_addr}:{https_port}')

    # Create sockets
    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_socket.bind((ip_addr, http_port))
    http_socket.listen(5)

    https_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    https_socket.bind((ip_addr, https_port))
    https_socket.listen(5)

    # SSL context for HTTPS
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    def accept_loop(socket, context=None):
        while True:
            client, address = socket.accept()
            if context:
                try:
                    client = context.wrap_socket(client, server_side=True)
                except ssl.SSLError:
                    print("SSL error occurred. Perhaps an HTTP client tried connecting to HTTPS server?")
                    client.close()
                    continue
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()

    # Start threads for HTTP and HTTPS
    http_thread = threading.Thread(target=accept_loop, args=(http_socket,))
    http_thread.start()

    https_thread = threading.Thread(target=accept_loop, args=(https_socket, context))
    https_thread.start()

if __name__ == '__main__':
    main()
