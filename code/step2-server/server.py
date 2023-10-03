import sys
import re

methods = ["GET", "POST", "PUT", "DELETE"]
httpVersions = ["HTTP/1.1", "HTTP/1.0"]
schemes = ["http", "https"]


def driver(ip_addr, port, cert_path, pk_path):
    print("IP: " , ip_addr)
    print("Port: " ,port)
    print("Cert Path: " , cert_path)
    print("Key Path: ", pk_path)

def main():
    ip_addr = sys.argv[1]
    port = sys.argv[2]
    cert_path = sys.argv[3]
    pk_path = sys.argv[4]

    driver(ip_addr, port, cert_path, pk_path)


main()