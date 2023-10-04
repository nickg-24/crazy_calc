import sys
import re
import socket
import ssl
import threading

methods = ["GET", "POST", "PUT", "DELETE"]
httpVersions = ["HTTP/1.1", "HTTP/1.0"]
schemes = ["http", "https"]


def driver(ip_addr, port, cert_path, pk_path):
    print("IP: " + ip_addr)
    print("Port: " + port)
    print("Cert Path: " + cert_path)
    print("Key Path: " + pk_path)


    # determine http vs https

# http version of handle, might not need to differentiate
def handle_client(client_socket):
    print("foo")

# https version of handle, might not need to differentiate
def handle(conn):
  print(conn.recv())
  conn.write(b'HTTP/1.1 200 OK\n\n%s' % conn.getpeername()[0].encode())

def main():
    ip_addr = sys.argv[1]
    port = sys.argv[2]

    is_https = True
    try:
        cert_path = sys.argv[3]
        pk_path = sys.argv[4]
    except IndexError:
        is_https = False

    #driver(ip_addr, port, cert_path, pk_path)

    print(is_https)
    
    if not is_https:
        # list on specified ip and port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip_addr, port))
        s.listen(5)
        while True:
            client, address = s.accept()
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()
    if is_https:
        sock = socket.socket()
        sock.bind((ip_addr,port))
        sock.listen(5)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=cert_path, keyfile=pk_path)
        context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
        while True:
            conn = None
            ssock, addr = sock.accept()
            try:
                conn = context.wrap_socket(ssock, server_side=True)
                handle(conn)
            except ssl.SSLError as e:
                print(e)
            finally:
                if conn:
                    conn.close()

    


main()