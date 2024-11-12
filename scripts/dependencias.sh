#!/bin/bash

apt install -y python3-venv python3-dev
apt install -y python3-pip
apt install -y python3-rpi.gpio
apt install -y dnsmasq hostapd 
apt install -y pigpio
apt install -y python3-matplotlib

pip3 install adafruit-circuitpython-dht Adafruit-Blinka
pip3 install -U python-magic

systemctl enable pigpiod
systemctl start pigpiod
