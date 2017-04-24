## Features
- Creates a GIF at the press of a button and saves it locally
- Optionally tweet the created GIF
- The GIF can be made to run START => END or "rebound" START <=> END
- Status LEDs keep the user informed as to what's going on

## Quick Links
 - [How to Use the Camera](#how-to-use-the-camera)
 - [Change Camera Behaviour](#change-camera-behaviour)
 - [Easy Installation](#easy-installation)
 - [3D Printer Files](#3d-printer-files)
 - [Connect your Pi Zero W to WiFi on first-boot](#pi-zero-w-wifi-and-ssh-on-first-boot)

## How to Use the Camera
- Power on the camera.
- The button will illuminate when the camera is ready to make a GIF.
- When you press the button, the button LED will strobe to indicate that the camera is recording.
- When recording finishes, the button LED will switch off.
- The status LED will blink while the GIF is being processed (and optionally, tweeted)
- When processing is finished, the camera will return to the READY state, and the button LED will illuminate.

## Change Camera Behaviour
The behaviour of the camera is controlled by a few _Behaviour Variables_. These are in `gifcam.py`.
With these variables you can change the frame-number and time duration of gifs, and control tweeting behaviour.
- `tweet = True/False` Enables or Disables an automatic tweet of the captured gif. This significantly increases the time needed in between GIF captures.
- `num_frame` Sets the number of frames in the gif
- `gif_delay` Sets the number of milliseconds a frame is displayed in the gif.
- `rebound = True/False` Create a gif that loops start <=> end

For now these variables are programmed into the script, but it would be trivial to connect extra switches to your Pi that control these variables. Perhaps a rotary switch to select frame number, and sliding switches to control rebound and tweet behaviour.

## 3D Printer Files:
- Download Here - http://www.thingiverse.com/thing:1761082


## Easy Installation
  - Make sure you're in the user directory: `cd ~`
  - Download the gifcam project: `wget https://github.com/CoreElectronics/gifcam/archive/master.zip`
  - unzip and rename the project: `unzip master.zip && mv gifcam-master gifcam`
  - Run the installer script: `sudo ~/gifcam/installer.sh` (This will take a long time if your pi needs to download updates
  - After installation finishes, the Pi will reboot.
  - Run the gifcam project to make sure everything works fine `python ~/gifcam/gifcam.py`
  - Proceed to [Twitter Configuration](#twitter-configuration)
  - Now proceed to [Run the gifcam at boot](#run-the-gifcam-at-boot)


## Manual Installation
  - Run -- `sudo apt-get update && sudo apt-get upgrade -y`
  - Install packages -- `sudo apt-get install python-picamera graphicsmagick python-pip git-core -y`
  - Install twython: `sudo pip install twython` -- https://github.com/ryanmcgrath/twython
  - Make sure camera interface is enabled with `sudo raspi-config` > Interfacing Options > Camera
  - Install GifCam -- `git clone https://github.com/michaelruppe/gifcam.git`

## Twitter Configuration
  - Create a twitter app at https://apps.twitter.com/ and populate `gifcam.py` with the necessary credentials. If you don't want to tweet your GIFs, don't create the app, and disable the functionality by setting `tweet = False` in `gifcam.py`.
  - Optional; Install mount USB if you want to use the `gifcamusb.py` script instead (no twitter, good for Pis without wifi. http://www.raspberrypi-spy.co.uk/2014/05/how-to-mount-a-usb-flash-disk-on-the-raspberry-pi/
  - To access your GIFs over WiFi, configure the gif directory as a samba shared directory


## Run the gifcam at boot:
  - Run -- `crontab -e`
    - You may be prompted to select a text editor if you haven't edited the crontab before. You'll be prompted for a selection between 1 and 3. I choose nano, which is 2 - this is also the default choice, indicated by the `[2]` .
  - add this line to end of that file - `@reboot sh /home/pi/gifcam/launcher.sh`
  
  
## Optional: Setup a Samba shared directory to access your GIFs over WiFi
  - Install samba: `sudo apt-get install samba samba-common-bin`
  - Create a backup of the default samba configuration: `sudo cp /etc/samba/smb.conf /etc/samba/smb.conf_$(date +%F)`
    This will create a copy, with today's date on the extension.
  -  Set the gif directory as a shared directory: `sudo nano /etc/samba/smb.conf` and add the following chunk:
  ```
  [gifs]
    comment = GIF share
    path = /home/pi/gifcam/gifs
    browseable = yes
    read only = no
  ```
  - Create samba users: execute `sudo smbpasswd -a pi` and enter your desired password. Whether you choose to keep this as the default (unsecure) is up to you. This will be the username and password required to access the shared folder.
  - Restart your samba service with `sudo /etc/init.d/smbd stop` then `sudo /etc/init.d/smbd start` (or just reboot with `sudo reboot`)
  - You can should now be able to access your networked drive. On Windows, enter \\gifcam into your explorer address bar and you should be prompted for the **samba** username and password you created earlier.
  
## Pi Zero W WiFi and SSH on first boot
These instructions will work for Raspberry Pis that have WiFi on-baord eg. Pi 3 B, Zero W.
**Complete the following steps on your computer. We will be creating and modifying files in the small "BOOT" partition of the SD card. On Windows, this is the drive that appears when you plug in your Raspbian SD card.**
  - Flash SD card with Jessie Lite
  - Open the SD card in your File Explorer.
  - Setup USB OTG network access. This will allow you to always SSH into the Pi via a direct connection through USB - useful if you have problems with WiFi at any point.
    - Open the file `config.txt` and add to the bottom `dtoverlay=dwc2` on a new line, then save the file.
    - Open `cmdline.txt`. Very careful with the syntax in this file: Each parameter is seperated by a single space (it does not use newlines). Insert `modules-load=dwc2,g_ether` after rootwait. Make sure there is a single space before and after this piece of text.
  - Setup WiFi access for first boot:
    - Create a file called `wpa_supplicant.conf` in the boot parition.
    - Paste the following text into the file, filling in your own WiFi SSID (network name) and password.
      ```
      network={
        ssid="SSID"
        psk="password"
        key_mgmt=WPA-PSK
      }
      ```
    - You can follow this process at any time to overwrite the WiFi credentials if you have to.
  - Enable SSH: create an empty file called `ssh` in the boot partition. Make sure there is no file extension.
  - Power the Pi and open an SSH session. If you're accessing over wifi, SSH to `pi@raspberrypi`. If you're accessing over USB OTG, SSH to `pi@raspberrypi.local`
  - On first boot give the Pi a meaningful hostname, like `gifcam`. This will avoid hostname conflicts on your network if you deploy another Raspberry Pi.
  - Now follow the _Basic Setup_ instructions


## ToDo:
- working directory referencing, this is so you can cleanup source images with: `rm $workingDir/\*.jpg` rather than from within the repo main directory
- smart twitter handling for when gifs are taken and you're not on wifi? If an image upload fails it gets pushed onto a re-attempt stack, which attempts to pop each time a gif is taken / an upload button pressed!
