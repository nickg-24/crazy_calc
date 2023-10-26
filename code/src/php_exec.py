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
def env_setup(method, script_filename, query_string="", post_body=""):
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
            'SCRIPT_FILENAME' : 'cgi-test2.php',
            'REQUEST_METHOD' : 'POST',
            'GATEWAY_INTERFACE' : 'CGI/1.1',
            'CONTENT_TYPE' : 'application/x-www-form-urlencoded'
        }

        if post_body:
            env['CONTENT_LENGTH'] = str(len(post_body))
        CONTENT_LENGTH="6" \
        echo "test=1" | php-cgi

