import re

# Predefined schemes
schemes = ["http", "https", "ftp", "tcp"]
# Reserved characters
reserved = [";", "/", ":", "@", "&", "=", "+", "$", ","]

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
    "/path/with/invalid^char",
    "/"
]

for test_uri in test_uris:
    print(f"'{test_uri}' is {'valid' if is_valid_uri(test_uri) else 'invalid'}")

