#!/bin/sh

cd broker && cargo build --release
cd ..
cd client && cargo build --release
cd ..

vagrant scp broker/target/ /home/vagrant/mqtt/broker/
vagrant scp client/target/ /home/vagrant/mqtt/client/
vagrant scp broker/src/genpem.sh /home/vagrant/mqtt/broker/genpem.sh
vagrant scp mqtt-mininet.py /home/vagrant/mqtt/mqtt-mininet.py
vagrant scp broker/src/config/rumqttd.conf /home/vagrant/mqtt/rumqttd.conf