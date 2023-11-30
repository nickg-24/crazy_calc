# Code Directory README
## Directory Structure
This directory consists of 5 subdirectories:

### logs
Contains ``valid_requests.log`` and ``internal_errors.log``. The ``valid_requests.log`` file contains the date, time, and first line of valid requests to the web server. Error logging to a a file is not implemented.

### src
Contains the source code for the web server.

### ssl
Contains the certificate and private key files for the server's https socket configuration.

### www
Contains web server files. Includes ``.html`` and ``.php`` files.

### z_misc
Contains old versions of the server, corresponding to the steps outlined in the assignment instructions. Chat GPT logs are included in the ``chat_gpt_logs`` directory

## Running the Server

### Start Up
To start the server run the following command from a terminal in the ``src`` directory. ``IP_ADDR`` is the the IP address that the server will accept connections from. ``0.0.0.0`` will accept connections from any IP address. ``PORT`` is the port that the server will accept standard HTTP connections from. By default the server will  establish an SSL socket listening on port 443 for connections originating from the specified ``IP_ADDR``.

```bash
$ sudo python3 server.py {IP_ADDR} {PORT}
```

### Operations
Complete HTTP requests will be outputted to the terminal. Valid requests to the server will be logged to ``code/logs/valid_requests.log``.

### Shut Down
There is no graceful shutdown method at this time. Exit the server process by pressing ``Ctrl + C``.

### Rubric
The ![hello-world.html](./www/hello-world.html) webpage allows you to quickly test GET and POST form submissions for ease of grading.