# this file handles the php execution.
# i wanted to separte this into another file to make the main server.py less messy

import server
import subprocess
import os

'''
Converting the stack overflow for GET from windows -> unix


For GET request: *works

QUERY_STRING="<parameter1>=<value1>&<parameter2>=<value2>&[...]&<parameterN>=<valueN>" \
SCRIPT_FILENAME="cgi-test2.php" \
REQUEST_METHOD="GET" \
REDIRECT_STATUS="0" \
php-cgi


For POST request *works (if errors happen, add export)

REDIRECT_STATUS="0" \
SCRIPT_FILENAME="cgi-test2.php" \
REQUEST_METHOD="POST" \
GATEWAY_INTERFACE="CGI/1.1" \
CONTENT_TYPE="application/x-www-form-urlencoded" \
CONTENT_LENGTH="6" \
echo "test=1" | php-cgi


'''

# sets up the environment variables 
def execute_php(method: str, script_filename: str, query_string: str="", post_body: str=""):
    relative_path = server.DOCUMENT_ROOT + '/' +script_filename
    # gets absolute path of php script
    abs_path = os.path.abspath(relative_path)

    # sets up GET env variables seen above
    if method == "GET":
        env = {
            'QUERY_STRING' : query_string,
            'SCRIPT_FILENAME' : abs_path,
            'REQUEST_METHOD' : method,
            'REDIRECT_STATUS' : '0'
        }
    # sets up POST env variables seen above
    if method == "POST":
        env = {
            'REDIRECT_STATUS' : '0',
            'SCRIPT_FILENAME' : abs_path,
            'REQUEST_METHOD' : 'POST',
            'GATEWAY_INTERFACE' : 'CGI/1.1',
            'CONTENT_TYPE' : 'application/x-www-form-urlencoded'
        }

        if post_body:
            env['CONTENT_LENGTH'] = str(len(post_body))

    # make the shell command
    proc = subprocess.Popen(
        ['php-cgi'],
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        env= env
    )

    if post_body:
        stdout_data, stderr_data = proc.communicate(input=post_body.encode())
    else:
        stdout_data, stderr_data = proc.communicate()
    #print(env)
    
    # print(stdout_data)

    # split stdout on \r\n\r\n , second part is the result
    output = stdout_data.decode().split('\r\n\r\n')[1]
    return output

def test_php_execution():
    script_path = "hello.php"
    
    # Test GET Request
    query_string = "name=Nick"
    print("Testing GET request:")
    print(execute_php("GET", script_path, query_string))
    
    # Test POST Request
    post_body = "param1=value1&param2=value2"
    print("Testing POST request:")
    print(execute_php("POST", script_path, post_body=post_body))

# for testing
def main():
    #execute_php("GET","../www/cgi-test2.php","<parameter1>=<value1>&<parameter2>=<value2>&<parameterN>=<valueN>")

    test_php_execution()

if __name__ == "__main__":
    main()