import sys
import re

methods = ["GET", "POST", "PUT", "DELETE", "HEAD"]
httpVersions = ["HTTP/1.1", "HTTP/1.0"]

def read_request(path):
    with open(path, 'r') as file:
        return file.read()

def validate(req_str):
    try:
        # check if blank
        if req_str == '':
            return 400
        
        # split the request into headers and body, if both are present
        parts = re.split(r'\r\n\r\n|\n\n', req_str, maxsplit=1)
        if len(parts) == 2:
            headers, body = parts
        else:
            headers = parts[0]
            body = ''

        # split on newlines and get rid of the \r if its there        
        normalized_lines = [line.rstrip('\r') for line in headers.split('\n')]

        # check num of parts in top_line
        top_line = normalized_lines.pop(0).split()
        if len(top_line) != 3:
            return 400
        # check that methods and version is good
        method = top_line[0]
        uri = top_line[1]
        version = top_line[2]
        if method not in methods:
            return 405
        if version not in httpVersions:
            return 505
        
        # check headers
        for line in normalized_lines:
            if ':' not in line:
                return 400
            head_name, head_value = line.split(':', 1)
            # check that head_name has no spaces
            for char in head_name:
                if char.isspace():
                    return 400

        # check body
        

        return 200
    
    # server error
    except Exception as e:
        print(f"Exception: {e}")
        return 500  # HTTP 500 Internal Server Error

def main():
    try:
        # getting the request
        path_2_req = sys.argv[1]
        r_req = read_request(path_2_req)

        # validating the request
        valid_code = validate(r_req)
    except:
        valid_code = 500
        
    # print output based on valid_code
    if valid_code == 400:
        print("HTTP/1.1 400 Bad Request")
    elif valid_code == 405:
        print("HTTP/1.1 405 Method Not Allowed")
    elif valid_code == 505:
        print("HTTP/1.1 505 HTTP Version Not Supported")
    elif valid_code == 200:
        print("HTTP/1.1 200 OK")
    else:
        print("HTTP/1.1 500 Internal Server Error")

main()