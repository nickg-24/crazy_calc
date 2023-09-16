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
        # split on newlines and get rid of the \r if its there        
        lines = req_str.split('\n')
        normalized_lines = [line.rstrip('\r') for line in lines]

        # check num of parts in top_line
        top_line = normalized_lines.pop(0).split()
        if len(top_line) != 3:
            return 400
        # check that methods and version is good
        method = top_line[0]
        uri = top_line[1]
        version = top_line[2]
        if method not in methods:
            return 400
        if version not in httpVersions:
            return 400
        
        # check headers


        # check body
        
    # server error
    except Exception as e:
        print(f"Exception: {e}")

def main():
    path_2_req = sys.argv[1]

    r_req = read_request(path_2_req)

    print(validate(r_req))

main()