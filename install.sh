#!/bin/sh

echo "getting cuneyt files from the repo"
git clone "https://github.com/hisarcs/cuneyt"

echo "installing i2c-tools"
apt-get install i2c-tools

echo "instaling git, python"
sudo apt-get install git build-essential python-dev

echo "upgrading pip"
pip install pip-upgrade

echo "downloading cuneyt libraries"
pip install tweepy
pip install pymongo
pip install pyglet
cd /home/pi
mkdir Adafruit_Python_PCA9685
git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git Adafruit_Python_PCA9685
cd Adafruit_Python_PCA9685
python setup.py install

cd /home/pi/Desktop
echo "creating resources and captures folders for cuneyt"
mkdir cuneyt/resources 
mkdir cuneyt/captures cuneyt/captures/images cuneyt/captures/videos

echo "creating configuration file for cuneyt"
echo "mongo_user = \"my_mongo_username\"
mongo_pass = \"my_mongo_password\"
mongo_url = \"my_mongo_url\"
log_file = \"log.txt\" #feel free to change the filename
backlog_file = \"backlog.csv\" #feel free to change the filename
resource_folder = \"resources\"
captures_folder = \"captures\"
twitter_consumer_key = \"my_consumer_key\"
twitter_consumer_secret = \"my_consumer_secret\"
twitter_access_token \ \"my_access_token\"
twitter_access_secret = \"my_access_secret\"" > cuneyt/config.py
      
echo "downloading required libraries"

echo "changing file permissions"
sudo chmod o=rwx cuneyt cuneyt/* cuneyt/.git
sudo chmod o=rwx home/pi/Adafruit_Python_PCA9685 ~/Adafruit_Python_PCA9685/*
echo "getting updates"
apt-get update

echo "getting upgrades"
apt-get upgrade
echo "updating your Raspberry Pi firmware"
rpi-update
echo "installation complete"

