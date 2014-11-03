trex - Toy Remote EXecution
===========================

A toy remote execution service.

Deploying 
---------

* Prerequisites: python3, virtualenv, pip

	$ git clone ...
	$ virtualenv .venv -p python3
	$ source .venv/bin/activate
	$ pip install -r requirements.txt

Configuring
-----------

The service uses port 9999 by default, so ensure this is available. The service
listens to incoming requests from any IP.

For each user, add a username, salted password, and one or more  programs the
user is authorized to run. For each program, add its corresponding path.

# sample.config

	[users]
	bob=1234, cat, ls
	
	[programs]
	cat=/bin/cat
	ls=/bin/ls

See the SSL section for details on configuring SSL mode.

Running
-------

## Server

	$ source .venv/bin/activate
	$ ./server sample.config
	
If you want to start in SSL mode, pass in the key and certificate file paths:

	$ ./server sample.config --ssl ssl/server.key ssl/server.crt

## Client

	$ source .venv/bin/activate
	$ ./client --server 127.0.0.1 --user bob --password 123 --exec ls

If you want to communicate with a server running in SSL mode, pass in the certificate file path:

	$ ./client --server 127.0.0.1 --user bob --password 123 --exec ls --ssl ssl/server.crt

SSL
---
Normally, the client communicates with the server in cleartext. Use the SSL
option to encrypt communications. The following assumes that you will be using
a self-signed certificate. In order for the SSL protocol to work, you must make
available (1) a private key to the server, and (2) a certificate to  to both
the server and client. For more information, see the following [tutorial](https://www.digitalocean.com/community/tutorials/how-to-create-a-ssl-certificate-on-apache-on-arch-linux).

* Prerequisites: openssl

1. Create a directory to store the key and certificate
	
	$ mkdir ssl

2. Create the private key
	
	$ openssl genrsa -des3 -out ssl/server.orig.key 2048

3. Remove the passphrase from the key, unless you can enter the passphrase
every time you start the server.
	
	$ openssl rsa -in ssl/server.orig.key -out ssl/server.key

4. Create the certificate-signing request
	
	$ openssl req -new -key ssl/server.key -out ssl/server.csr

5. Create the certificate
	
	$ openssl x509 -req -days 365 -in ssl/server.csr -signkey ssl/server.key -out ssl/server.crt
	