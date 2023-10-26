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
    # sets up GET env variables seen above
    if method == "GET":
        env = {
            'QUERY_STRING' : query_string,
            'SCRIPT_FILENAME' : script_filename,
            'REQUEST_METHOD' : method,
            'REDIRECT_STATUS' : '0'
        }
    # sets up POST env variables seen above
    if method == "POST":
        env = {
            'REDIRECT_STATUS' : '0',
            'SCRIPT_FILENAME' : script_filename,
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
    print(env)
    print(stdout_data)

# for testing
def main():
    
    execute_php("GET","../www/cgi-test2.php","<parameter1>=<value1>&<parameter2>=<value2>&<parameterN>=<valueN>")
    print(os.system('pwd'))
    print(os.system('ls ../www'))
    print(os.system('find ../www/cgi-test2.php'))

if __name__ == "__main__":
    main()