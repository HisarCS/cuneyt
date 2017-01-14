#!/bin/sh

echo "getting cuneyt files from the repo"
git clone "https://github.com/hisarcs/cuneyt"

echo "upgrading pip"
pip install pip-upgrade

echo "creating resources and captures folders for cuneyt"
mkdir cuneyt/resources 
mkdir cuneyt/captures cuneyt/captures/images cuneyt/captures/videos

echo "creating configuration file for cuneyt"
echo "\"mongo_user\" = \"my_mongo_username\"
\"mongo_pass\" = \"my_mongo_password\"
\"mongo_url\" = \"my_mongo_url\"
\"log_file\" = \"log.txt\" #feel free to change the filename
\"backlog_file\" = \"backlog.csv\" #feel free to change the filename
\"resource_folder\" = \"resources\"
\"captures_folder\" = \"captures\"" > config.py
      
echo "downloading required libraries"

echo "increasing gpu memory"
CONFIG_FILE="config.txt"
TARGET_KEY="gpu_mem"
REPLACEMENT_VALUE="256"
sed -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE

echo "enabling RPi camera"
TARGET_KEY="start_x"
REPLACEMENT_VALUE="1"
sed -i "s/\($TARGET_KEY *= *\).*/\1$REPLACEMENT_VALUE/" $CONFIG_FILE

echo "enabling RPi I2C"
TARGET_KEY="^device_tree_param="
ALT_KEY="^dtparam="
if grep -Fq "$TARGET_KEY" $CONFIG_FILE
then
	echo "device_tree_param already exists"
else
	if grep -Fq "$ALT_KEY" $CONFIG_FILE
	then
		echo "dtparam already exists"
	else
		echo "dtparam=i2c=1" > $CONFIG_FILE
	fi
fi

echo "getting updates"
apt-get update

echo "getting upgrades"
apt-get upgrade
echo "updating your Raspberry Pi firmware"
rpi-update


