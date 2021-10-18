#!/bin/sh

dir=tlsfiles/

rm -rf $dir
mkdir $dir

openssl genrsa 2048 > ${dir}ca.key.pem
openssl req -new -x509 -nodes -days 365000 -key ${dir}ca.key.pem -out ${dir}ca.cert.pem
openssl req -newkey rsa:2048 -nodes -days 365000 -keyout ${dir}server.key.pem -out ${dir}server.req.pem
openssl x509 -req -days 365000 -set_serial 01 -in ${dir}server.req.pem -out ${dir}server.cert.pem -CA ${dir}ca.cert.pem -CAkey ${dir}ca.key.pem