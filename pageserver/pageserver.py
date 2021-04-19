"""
  A trivial web server in Python.

  Based largely on https://docs.python.org/3.4/howto/sockets.html
  This trivial implementation is not robust:  We have omitted decent
  error handling and many other things to keep the illustration as simple
  as possible.

  FIXME:
  Currently this program always serves an ascii graphic of a cat.
  Change it to serve files if they end with .html or .css, and are
  located in ./pages  (where '.' is the directory from which this
  program is run).
"""

import _thread   # Response computation runs concurrently with main program
import socket    # Basic TCP/IP communication on the internet
import config    # Configure from .ini files and command line
import os
import os.path
import logging   # Better than print statements
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)
# Logging level may be overridden by configuration


def listen(portnum):
    """
    Create and listen to a server socket.
    Args:
       portnum: Integer in range 1024-65535; temporary use ports
           should be in range 49152-65535.
    Returns:
       A server socket, unless connection fails (e.g., because
       the port is already in use).
    """
    # Internet, streaming socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to port and make accessible from anywhere that has our IP address
    serversocket.bind(('', portnum))
    serversocket.listen(1)    # A real server would have multiple listeners
    return serversocket


def serve(sock, func):
    """
    Respond to connections on sock.
    Args:
       sock:  A server socket, already listening on some port.
       func:  a function that takes a client socket and does something with it
    Returns: nothing
    Effects:
        For each connection, func is called on a client socket connected
        to the connected client, running concurrently in its own thread.
    """
    while True:
        log.info("Attempting to accept a connection on {}".format(sock))
        (clientsocket, address) = sock.accept()
        _thread.start_new_thread(func, (clientsocket,))


##
# Starter version only serves cat pictures. In fact, only a
# particular cat picture.  This one.
##
CAT = """
     ^ ^
   =(   )=
"""

# HTTP response codes, as the strings we will actually send.
# See:  https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
# or    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
##
STATUS_OK = "HTTP/1.0 200 OK\n\n"
STATUS_FORBIDDEN = "HTTP/1.0 403 Forbidden\n\n"
STATUS_NOT_FOUND = "HTTP/1.0 404 Not Found\n\n"
STATUS_NOT_IMPLEMENTED = "HTTP/1.0 401 Not Implemented\n\n"


def respond(sock):
    """
    This server responds only to GET requests (not PUT, POST, or UPDATE).
    Any valid GET request is answered with an ascii graphic of a cat.
    """
    sent = 0
    request = sock.recv(1024)  # We accept only short requests
    request = str(request, encoding='utf-8', errors='strict')
    log.info("--- Received request ----")
    log.info("Request was {}\n***\n".format(request))

    parts = request.split()
    print("parts:", parts)
    if len(parts) > 1 and parts[0] == "GET":
        # if parts[1] is in pages, transmit that content
        options = get_options()
        path = options.DOCROOT
        file_name = parts[1][1:]
        print("file_name:", file_name)
        # does it start with a forbidden char?
        # use split and a loop for robustness in directories
        forbidden = False
        pieces = file_name.split('/')
        for piece in pieces:
            if len(piece) < 1:
                transmit(STATUS_OK, sock)
                transmit(STATUS_FORBIDDEN, sock)
                forbidden = True
                break
            elif (piece[0] == '~') or (piece[0] == '/') or (piece[0] == '.' and piece[1] == '.'):
                transmit(STATUS_OK, sock)
                transmit(STATUS_FORBIDDEN, sock)
                forbidden = True
                break
        if forbidden == False:
            source_path = os.path.join(path, file_name)
            if file_name in os.listdir(path):
                # if os.path.isfile(source_path):
                # print("file is in pages!")
                if (file_name[-4:] == 'html') or (file_name[-3:] == 'css'):
                    # print("it's html or css!")
                    transmit(STATUS_OK, sock)
                    with open(source_path, "r") as file:
                        # print("file contents: ", file.read()) # for some reason this fails the test
                        transmit(file.read(), sock)
                        # for line in file.readlines():
                        #     print("line: ", line)
                        #     transmit(line, sock)
            else:
                transmit(STATUS_OK, sock)
                transmit(STATUS_NOT_FOUND, sock)
                # else:
                #     transmit(STATUS_OK, sock)
                #     transmit(CAT, sock)
    else:
        log.info("Unhandled request: {}".format(request))
        transmit(STATUS_NOT_IMPLEMENTED, sock)
        transmit("\nI don't handle this request: {}\n".format(request), sock)

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    return


def transmit(msg, sock):
    """It might take several sends to get the whole message out"""
    sent = 0
    while sent < len(msg):
        buff = bytes(msg[sent:], encoding="utf-8")
        sent += sock.send(buff)

###
#
# Run from command line
#
###


def get_options():
    """
    Options from command line or configuration file.
    Returns namespace object with option value for port
    """
    # Defaults from configuration files;
    #   on conflict, the last value read has precedence
    options = config.configuration()
    # We want: PORT, DOCROOT, possibly LOGGING

    if options.PORT <= 1000:
        log.warning(("Port {} selected. " +
                     " Ports 0..1000 are reserved \n" +
                     "by the operating system").format(options.port))

    return options


def main():
    options = get_options()
    port = options.PORT
    if options.DEBUG:
        log.setLevel(logging.DEBUG)
    sock = listen(port)
    log.info("Listening on port {}".format(port))
    log.info("Socket is {}".format(sock))
    serve(sock, respond)


if __name__ == "__main__":
    main()
