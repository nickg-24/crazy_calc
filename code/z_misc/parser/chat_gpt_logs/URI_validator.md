**You:**

I am going to give you a section of RFC 2616 which talks about the formatting of uris in an http request:
3.2 Uniform Resource Identifiers

   URIs have been known by many names: WWW addresses, Universal Document
   Identifiers, Universal Resource Identifiers [3], and finally the
   combination of Uniform Resource Locators (URL) [4] and Names (URN)
   [20]. As far as HTTP is concerned, Uniform Resource Identifiers are
   simply formatted strings which identify--via name, location, or any
   other characteristic--a resource.



Fielding, et al.            Standards Track                    [Page 18]


RFC 2616                        HTTP/1.1                       June 1999


3.2.1 General Syntax

   URIs in HTTP can be represented in absolute form or relative to some
   known base URI [11], depending upon the context of their use. The two
   forms are differentiated by the fact that absolute URIs always begin
   with a scheme name followed by a colon. For definitive information on
   URL syntax and semantics, see "Uniform Resource Identifiers (URI):
   Generic Syntax and Semantics," RFC 2396 [42] (which replaces RFCs
   1738 [4] and RFC 1808 [11]). This specification adopts the
   definitions of "URI-reference", "absoluteURI", "relativeURI", "port",
   "host","abs_path", "rel_path", and "authority" from that
   specification.

   The HTTP protocol does not place any a priori limit on the length of
   a URI. Servers MUST be able to handle the URI of any resource they
   serve, and SHOULD be able to handle URIs of unbounded length if they
   provide GET-based forms that could generate such URIs. A server
   SHOULD return 414 (Request-URI Too Long) status if a URI is longer
   than the server can handle (see section 10.4.15).

      Note: Servers ought to be cautious about depending on URI lengths
      above 255 bytes, because some older client or proxy
      implementations might not properly support these lengths.

3.2.2 http URL

   The "http" scheme is used to locate network resources via the HTTP
   protocol. This section defines the scheme-specific syntax and
   semantics for http URLs.

   http_URL = "http:" "//" host [ ":" port ] [ abs_path [ "?" query ]]

   If the port is empty or not given, port 80 is assumed. The semantics
   are that the identified resource is located at the server listening
   for TCP connections on that port of that host, and the Request-URI
   for the resource is abs_path (section 5.1.2). The use of IP addresses
   in URLs SHOULD be avoided whenever possible (see RFC 1900 [24]). If
   the abs_path is not present in the URL, it MUST be given as "/" when
   used as a Request-URI for a resource (section 5.1.2). If a proxy
   receives a host name which is not a fully qualified domain name, it
   MAY add its domain to the host name it received. If a proxy receives
   a fully qualified domain name, the proxy MUST NOT change the host
   name.








Fielding, et al.            Standards Track                    [Page 19]


RFC 2616                        HTTP/1.1                       June 1999


3.2.3 URI Comparison

   When comparing two URIs to decide if they match or not, a client
   SHOULD use a case-sensitive octet-by-octet comparison of the entire
   URIs, with these exceptions:

      - A port that is empty or not given is equivalent to the default
        port for that URI-reference;

        - Comparisons of host names MUST be case-insensitive;

        - Comparisons of scheme names MUST be case-insensitive;

        - An empty abs_path is equivalent to an abs_path of "/".

   Characters other than those in the "reserved" and "unsafe" sets (see
   RFC 2396 [42]) are equivalent to their ""%" HEX HEX" encoding.

   For example, the following three URIs are equivalent:

      http://abc.com:80/~smith/home.html
      http://ABC.com/%7Esmith/home.html
      http://ABC.com:/%7esmith/home.html

Now I am going to give you a script that my professor gave me to serve as a sample for parsing and determining the validity of uris:
import sys


methods = ["GET", "POST", "CONNECT"]
httpVersions = ["HTTP/1.1", "HTTP/1.0"]
reserved = [";", "/", ":", "@", "&amp;", "=", "+", "$", ","]
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


Using both the excerpt from the rfc and the sample script from my professor, give me a list of things that would make a uri valid or invalid. I also want you to write code for a script that determines the validity of a uri. Assume that the input for the new script is a singular string. 

Things to keep in mind for this script: make sure to refer to the section from RFC 2616. Also check for the things my professor checked for in terms of uri validation. Check to make sure that uris are correctly split and parsed. Additionally provides test cases that contain valid and invalid uri strings

------------------

**ChatGPT:**

Based on the provided excerpt from RFC 2616 and the sample script from your professor, here's a list of things that determine the validity of a URI:

### Valid URI Criteria:

- URIs can be in the form of an absolute URI, an abs_path, an authority, or a "*".
- Absolute URIs always begin with a scheme name followed by a colon.
- The path in the URI should begin with a "/".
- The characters in the URI should be alphanumeric, spaces, or reserved characters (i.e., ";", "/", ":", "@", "&", "=", "+", "$", ",").
- The scheme of the URI should be one of the predefined schemes (e.g., "http", "https", "ftp", "tcp").
- The authority part of the URI can be a hostname (e.g., "localhost", "somedomain.com") or an IP address.
- The HTTP protocol does not place any a priori limit on the length of a URI. However, servers should be cautious about depending on URI lengths above 255 bytes.
- Comparisons of host names must be case-insensitive.
- Comparisons of scheme names must be case-insensitive.
- An empty abs_path is equivalent to an abs_path of "/".
- Characters other than those in the "reserved" and "unsafe" sets are equivalent to their "%" HEX HEX encoding.

### Invalid URI Criteria:

- If the URI does not match any of the valid forms (absolute URI, abs_path, authority, "*").
- If the URI contains characters other than alphanumeric, spaces, or reserved characters and is not properly encoded.
- If the scheme of the URI is not one of the predefined schemes.
- If the authority part of the URI contains invalid characters.
- If the URI length exceeds the server's handling capacity.

Now, let's write a script to determine the validity of a URI based on the above criteria:

```python
import re

# Predefined schemes
schemes = ["http", "https", "ftp", "tcp"]
# Reserved characters
reserved = [";", "/", ":", "@", "&amp;", "=", "+", "$", ","]

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

# Test cases
test_uris = [
    "http://localhost:8080/path/to/resource",
    "https://somedomain.com",
    "ftp://1.2.3.4/",
    "/path/to/resource",
    "localhost",
    "*",
    "http:://invalid_scheme.com",
    "http://invalid^authority.com",
    "/path/with/invalid^char"
]

for test_uri in test_uris:
    print(f"'{test_uri}' is {'valid' if is_valid_uri(test_uri) else 'invalid'}")


```
This script defines the `is_valid_uri` function that checks the validity of a URI based on the criteria mentioned above. The test cases at the end of the script contain both valid and invalid URI strings.



------------------

