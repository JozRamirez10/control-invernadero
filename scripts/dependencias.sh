#!/bin/bash

pip3 install adafruit-circuitpython-dht Adafruit-Blinka
python3 -m pip install pigpio

apt-get install dnsmasq hostapd -y
pip3 install -U python-magic