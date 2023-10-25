# this file handles the php execution.
# i wanted to separte this into another file to make the main server.py less messy

import server

DOCUMENT_ROOT = server.DOCUMENT_ROOT

'''
Converting the stack overflow for GET from windows -> unix

export QUERY_STRING="<parameter1>=<value1>&<parameter2>=<value2>&[...]&<paramterN>=<valueN>"
export SCRIPT_NAME="<script-file-name>"
export REQUEST_METHOD="GET"
export REDIRECT_STATUS="0"
php-cgi
'''