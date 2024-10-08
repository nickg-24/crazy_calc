import sys
import re

methods = ["GET", "POST", "PUT", "DELETE", "HEAD"]
httpVersions = ["HTTP/1.1", "HTTP/1.0"]
schemes = ["http", "https", "ftp", "tcp"]
reserved = [";", "/", ":", "@", "&", "=", "+", "$", ",", ".", "?", "-", "_", "%"]

def read_request(path):
    with open(path, 'r') as file:
        return file.read()

def is_valid_uri(uri):
    # Check for "*" form
    if uri == "*":
        return True
    
    # Check for absolute URI form
    if any(uri.startswith(scheme + "://") for scheme in schemes):
        # Extract authority and path
        parts = uri.split("://", 1)[1].split("/", 1)
        authority = parts[0]
        path = "/" + parts[1] if len(parts) > 1 else "/"
        # Validate authority and path
        if not re.match(r'^[a-zA-Z0-9-._~:]*$', authority):
            return False
        if not all(c.isalnum() or c in reserved for c in path):
            return False
        return True
    
    # Check for abs_path form
    if uri.startswith("/"):
        if not all(c.isalnum() or c in reserved for c in uri):
            return False
        return True
    
    # Check for authority form
    if re.match(r'^[a-zA-Z0-9-._~:]*$', uri):
        return True
    
    return False

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
        
        # check uri
        if is_valid_uri(uri) == False:
            return 400

        # flag to check for Content-Length
        has_content_length = False

        # print("normalized_lines", normalized_lines) # testing
        # check headers
        for line in normalized_lines:
            if ':' not in line:
                return 400
            head_name, head_value = line.split(':', 1)

            # print("head_name", head_name) # testing
            # print("head_value", head_value) # testing
            # check for Content-Length
            if head_name.strip().lower() == "content-length":
                has_content_length = True
                # print("has_content_length",has_content_length) # testing

            '''This part is broken 
            # make sure that post requests are www-form-urlencoded
            if head_name.strip().lower() == "content-type":
                if head_value != "application/x-www-form-urlencoded" and method == "POST":            
                    return 415
            '''

            # check that head_name has no spaces
            for char in head_name:
                if char.isspace():
                    return 400
        # make sure that post requests have a content length set
        if method == "POST" and not has_content_length:
            return 411
        
        # return status code 200, the method, and the uri
        return 200, method, uri, body
    
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
        valid_result = validate(r_req)
        if isinstance(valid_result, tuple) and len(valid_result) == 3:
            status_code, method, uri = valid_result
        else:
            status_code = valid_result
    except:
        status_code = 500
        
    # print output based on status_code
    if status_code == 400:
        print("HTTP/1.1 400 Bad Request")
    elif status_code == 405:
        print("HTTP/1.1 405 Method Not Allowed")
    elif status_code == 505:
        print("HTTP/1.1 505 HTTP Version Not Supported")
    elif status_code == 200:
        print("HTTP/1.1 200 OK")
    elif status_code == 411:
        print("HTTP/1.1 411 Content Length Required")
    else:
        print(f"Status Code: {status_code}")
        print("HTTP/1.1 500 Internal Server Error")

if __name__ == '__main__':
    main()
