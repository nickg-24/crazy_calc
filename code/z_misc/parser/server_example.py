import sys


methods = ["GET", "POST", "CONNECT"]
httpVersions = ["HTTP/1.1", "HTTP/1.0"]
reserved = [";", "/", ":", "@", "&", "=", "+", "$", ","]
schemes=["http", "https", "ftp", "tcp"]
	
def isPath(uri):
	#Per RFC 2396:
	#<path>?<query>
	#Note - Path begins with /
	#Note that anything beyond / is optional, including a query
	if not uri[0] == '/':
		return False 
	for letter in uri:
		if not letter.isalpha() and not letter.isnumeric() and not letter ==" " and not letter in reserved:
			return False
	return True

def isAbsolute(uri):
	#Per RFC 2396:
	#<scheme>://<authority><path>?<query>
	#Note: Authority is localhost, 1.2.3.4, somedomain.com, etc. 
	#Path/query are both optional.

	for scheme in schemes:
		if len(scheme) >= len(uri):
			pass
		elif not scheme == uri[0:len(scheme)]:
			pass
		else:
			restOfUri = uri[len(scheme):]
			#Case: Cannot possibly have both :// and an authority
			if len(restOfUri) < 4:
				return False
			#Case: Does not have ://	
			if restOfUri[0:3]!="://":
				return False	
			restOfUri = restOfUri[3:]
			
			#Verify that the is something which could be considered an authority
			if len(restOfURI):
				for letter in restOfUri:
					if not letter.isalpha() and not letter.isnumeric() and not letter ==" " and not letter in reserved:
						return False #Handle the case where the authority/path contains an invalid symbol
				#We have verified there is a scheme followed by :// and some string which may be an authority/path/query
				#Any further work with the authority/path/query needs to be done by the part of the application 
				#which implements the handler for the request method.
				return True 

def isAuthority(uri):
	if len(uri) < 1:
		return False
	else:
		for letter in uri:
			if not letter.isalpha() and not letter.isnumeric() and not letter ==" " and not letter in reserved:
				return False
		return True	

def parseURI(uri):
	#Request-URI    = "*" | absoluteURI | abs_path | authority
	if uri =="*":
		return ""
	elif isPath(uri):	#abs_path
		return ""
	elif len(uri) > 7 and isAbsolute(uri):	
		return ""
	elif isAuthority(uri):
		return ""
	else:
		return "HTTP/1.1 400 Bad Request\r\n"
	

def parseRequestLine(line):
	parts = line.split(" ")
	if not parts[0] in methods:
		return "HTTP/1.1 405 Method Not Allowed\r\n"
	res = parseURI(parts[1])
	if not res:
		return res
	if not parts[2] in httpVersions:
		print(parts[2])
		return "HTTP/1.1 505 HTTP Version Not Supported\r\n"
	return ""
	
def parseHeader(line):
	print("Parse header: " + line)
	return "" #return nothing if there is no error

def parseRequest(requestLines):
	res = parseRequestLine(requestLines[0])
	if not res:
		linecount=1
		while requestLines[linecount]:
			res = parseHeader(requestLines[linecount])
			linecount=linecount+1
	if not res:
		res="HTTP/1.1 200 OK\r\n"
	return res

def getData(fn):
	req = ""
	with open(fn, "rb") as f:
		byte = f.read(1)
		req = req + str(byte.decode())
		while byte != b"":
			byte = f.read(1)
			req = req + str(byte.decode())
	return req
	

def main():
	reqfile = sys.argv[1]
	rawdata=getData(reqfile)
	reqLines = rawdata.split("\r\n")
	res = parseRequest(reqLines)
	print(res)

main()
