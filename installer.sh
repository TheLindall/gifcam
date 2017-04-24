#!/bin/sh
# installer.sh will install the necessary packages to get the gifcam up and running with 
# basic functions

# Install packages
PACKAGES="python-picamera graphicsmagick python-pip"
apt-get update
apt-get upgrade -y
apt-get install $PACKAGES -y
pip install twython


## Enable Camera Interface
CONFIG="/boot/config.txt"

# If a line containing "start_x" exists
if grep -Fq "start_x" $CONFIG
then
	# Replace the line
	echo "Modifying start_x"
	sed -i "s/start_x=0/start_x=1/g" $CONFIG
else
	# Create the definition
	echo "start_x not defined. Creating definition"
	echo "start_x=1" >> $CONFIG
fi

# If a line containing "gpu_mem" exists
if grep -Fq "gpu_mem" $CONFIG
then
	# Replace the line
	echo "Modifying gpu_mem"
	sed -i "/gpu_mem/c\gpu_mem=128" $CONFIG
else
	# Create the definition
	echo "gpu_mem not defined. Creating definition"
	echo "gpu_mem=128" >> $CONFIG
fi


echo "Install complete, rebooting."
reboot
