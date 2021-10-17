#!/bin/sh

rm -rf tlsfiles/
mkdir tlsfiles/

openssl genrsa 2048 > tlsfiles/ca.key.pem
openssl req -new -x509 -nodes -days 365000 -key tlsfiles/ca.key.pem -out tlsfiles/ca.cert.pem
openssl req -newkey rsa:2048 -nodes -days 365000 -keyout tlsfiles/server.key.pem -out tlsfiles/server.req.pem
openssl x509 -req -days 365000 -set_serial 01 -in tlsfiles/server.req.pem -out tlsfiles/server.cert.pem -CA tlsfiles/ca.cert.pem -CAkey tlsfiles/ca.key.pem