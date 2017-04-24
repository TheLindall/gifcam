#!/bin/sh
# installer.sh will install the necessary packages to get the gifcam up and running.
# If you want Samba shared folders or USB drive support you will have to follow the instructions on
# https://github.com/CoreElectronics/gifcam

# Packages to install
PACKAGES="python-picamera graphicsmagick python-pip"

apt-get update
apt-get upgrade -y
apt-get install $PACKAGES -y
pip install twython

###########
# TODO: fix - camera parameters aren't in boot.txt to begin with, so following code doesn't work
###########

# Make sure camera interface is enabled
if grep "start_x=1" /boot/config.txt
then
	break
else
	sed -i "s/start_x=0/start_x=1/g" /boot/config.txt
fi
# Camera requires 128MB GPU memory. Search for the gpu_mem parameter and replace the line.
if grep "gpu_mem=128" /boot/config.txt
then
	break
else
	sed -i "/gpu_mem/c\gpu_mem=128" /boot/config.txt
fi

echo "Install complete, rebooting."
reboot
