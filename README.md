## What's this version got?
This a minor de-update based on Nick and Michael's work. 
- I've removed the Twitter integration of the original projects
- I've added the hardware controls to change cmaera behaviors 
- I've added intructions to download your GIFs straight to your iPhone
- Used newer hardware (Rapberry Pi Zero W 2)
- Used newer software (Raspberry Pi OS Legacy Light - Buster)   

If you want:
- Auto twitter upload
- SSH instructions 
- A simplier setup
I suggest looking at the original projects by Nick (https://github.com/nickbrewer/gifcam) and <br>Micheal (https://github.com/michaelruppe/gifcam)

If you want to see the orginal project and build instructions see here (https://www.hackster.io/nick-brewer/pix-e-gif-camera-323965)


## Features
- Creates a GIF at the press of a button and saves it locally
- Access the GIFs through Samba and WiFi
- Use buttons to change capture parameters
  —
- The GIF can be made to run START => END or "rebound" START <=> END
- Status LEDs keep the user informed as to what's going on

## Camera hardware requirements
The code assumes a few things about your camera's design:
- There is a front facing LED (recording LED) (This was added so your subjects know when you are recording)
- There is a operator facing LED (status LED) (this was added so it was easier to see the status on a bright sunny day)
- There is a LED in the shutter button
- There are 4 toggle switches for controlling features

## How to Use the Camera
- Power on the camera.
- The shutter and status LEDs will turn on when the camera is ready to make a GIF.
- When you press the shutter button the recording LED will turn on solid, the status and shutter button will begin to blink while capturing. 
- When recording finishes, the status LED will blink rapidly, indicating it is processing.
- When processing is finished, the camera will return to the READY state, and the shutter button and status LED's will turn on solid.

## Change Camera Behaviour
Some of the variables are tied to physical switches, these can be edited in 'gifcma.py'. By default these are the behaviors:
- Switch 1 : Changed the number of frames captured between 12 (off) and 24 (on)
- Switch 2: Toggles the rebound behavior 
- Switch 3: Toggles what effects can be applied, it modifies switch 4
- Switch 4: Toggles the effects: If switch 3 if off (off = no fx, on = film grain), if Switch 3 is on ( off = soloraize, on = funny colorswap)

You can change the effects by chnaging the names in the code. For a refrence of the possible effects see "PiCamera.IMAGE_EFFECTS" here:
https://picamera.readthedocs.io/en/release-1.13/api_camera.html

---

# Basic Setup


## Raspberry Pi setup as of this writing
  - **Model:** Raspberry Pi Zero W 2 
  - **OS:** Raspberry Pi OS Legacy Lite (Buster)


## New to Raspberry Pi & and setting up your Pi with a monitor: 
If you are setting up your Rapsberry Pi Zero for the first time, with a monitor, and you didn't pre-configure anythign do this:
  - Use the command `sudo raspi-config` to: 
    -   Change your keyboard layout to to match yours
    -   Connect to your WiFi network
    -   Change the hostname to something like gifcam (just makes it easier to identify on the network)


## Install dependencies
Use the following commands to get GifCam up and running
  - Run: `sudo apt-get update -y`
  - Run: `sudo apt-get upgrade -y`
  - Enable the camera interface: `sudo raspi-config` > Interfacing Options > Camera > Yes
  - Install PiCamera: `sudo apt-get install python-picamera -y`
  - Install GraphicsMagick: `sudo apt-get install graphicsmagick -y`
  - Install Gitcore: `sudo apt-get install git-core`
  - Install GifCam: `git clone https://github.com/thelindall/gifcam.git`

## Setup a Samba shared directory to access your GIFs over WiFi 
  - Install samba: `sudo apt-get install samba samba-common-bin -y`
  - Create a backup of the default samba configuration: <br> `sudo cp /etc/samba/smb.conf /etc/samba/smb.conf_$(date +%F)` <br> This will create a copy, with today’s date on the extension.
  -  Set the gif directory as a shared directory: <br> `sudo nano /etc/samba/smb.conf` <br> and add the following chunk to the bottom of the doc: <br>

```
[gifs]
  comment = GIF share
  path = /home/pi/gifcam/gifs
  browseable = yes
  read only = no
```
  - Create a samba user: `sudo smbpasswd -a pi` and enter your desired password. Whether you choose to keep this as the default (unsecure) is up to you. This will be the username and password required to access the shared folder.
  - Restart your samba service with `sudo /etc/init.d/smbd stop` then `sudo /etc/init.d/smbd start` (or just reboot with `sudo reboot`)
  - You should now be able to access your networked drive. 
  - You can access the server from your iPhone as well. 
    - Use `sudo hostname -I` to find the IP address for your Raspberry pi.
    - Make sure your iPhone is connected to the same WiFi network as your Raspberry Pi
    - Open the Files app on your iphone and select "Connect to server" from the top-right menu.
    - Enter "smb://[your Pi's IP here]" into the Server field and then use the Samba user credentials you just set up.
    - This can be a bit finicky, you may need to close the files app, or eject and re-connect to the server. 
  - On Windows, enter \\gifcam into your explorer address bar and you should be prompted for the **samba** username and password you created earlier.


## Run the gifcam at boot
  - Run: `crontab -e`
    - You may be prompted to select a text editor if you haven't edited the crontab before. You'll be prompted for a selection between 1 and 3. I choose nano, which is 2 - this is also the default choice, indicated by the `[2]` .
  - add this line to end of that file - `@reboot sh /home/pi/gifcam/launcher.sh`

### Permissions
  - If hitting "permission denied" run: `Sudo shown -R pi/home/pi/gifcam`
