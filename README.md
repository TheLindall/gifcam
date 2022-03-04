## Features
- Creates a GIF at the press of a button and saves it locally
- Access the GIFs through Samba and WiFi
- Use buttons to change capture parameters
  —
- The GIF can be made to run START => END or "rebound" START <=> END
- Status LEDs keep the user informed as to what's going on

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


---

# Basic Setup


### Raspberry Pi setup as of this writing

  - **Model:** Raspberry Pi Zero W 2 
  - **OS:** Raspberry Pi Os Legacy Lite (Buster)


## Pi first boot w/ monitor
If you are setting up your Rapsberry Pi Zero for the first time:
  - Use he command `sudo raspi-config` to: 
    -   Change your keyboard layout to the correct one
    -   Connect to your WiFi network
    -   Change the hostname to something like gifcam


## Installing dependencies
  - Run: `sudo apt-get update -y`
  - Run: `sudo apt-get upgrade -y`
  - Enable the camera interface: `sudo raspi-config` > Interfacing Options > Camera > Yes
  - Install PiCamera: `sudo apt-get install python-picamera -y`
  - Install GraphicsMagick: `sudo apt-get install graphicsmagick -y`
  - Install Gitcore: `sudo apt-get install git-core`
  - Install GifCam: `git clone https://github.com/thelindall/gifcam.git`


## Setup a Samba shared directory to access your GIFs over WiFi 
  - Install samba: `sudo apt-get install samba samba-common-bin`-y
  - Create a backup of the default samba configuration: <br> `sudo cp /etc/samba/smb.conf /etc/samba/smb.conf_$(date +%F)` <br> This will create a copy, with today’s date on the extension.
  -  Set the gif directory as a shared directory: <br> `sudo nano /etc/samba/smb.conf` <br> and add the following chunk: <br>

```
[gifs]
  comment = GIF share
  path = /home/pi/gifcam/gifs
  browseable = yes
  read only = no
```
  - Create samba users: execute `sudo smbpasswd -a pi` and enter your desired password. Whether you choose to keep this as the default (unsecure) is up to you. This will be the username and password required to access the shared folder.
  - Restart your samba service with `sudo /etc/init.d/smbd stop` then `sudo /etc/init.d/smbd start` (or just reboot with `sudo reboot`)
  - You can should now be able to access your networked drive. 
  -You can access the server from your iPhone as well. You wil l need the IP address of your Raspberry Pi, you can find this by using the command`sudo hostname -I` . Once you have the IP address open the file app and sellect "Connect to server" from the top-right menu. From there enter `smb://[your ip]` and the credentials.
  -On Windows, enter \\gifcam into your explorer address bar and you should be prompted for the **samba** username and password you created earlier.


## Run the gifcam at boot
  - Run: `crontab -e`
    - You may be prompted to select a text editor if you haven't edited the crontab before. You'll be prompted for a selection between 1 and 3. I choose nano, which is 2 - this is also the default choice, indicated by the `[2]` .
  - add this line to end of that file - `@reboot sh /home/pi/gifcam/launcher.sh`

### Permissions
  - If hitting "permission denied" run: `Sudo shown -R pi/home/pi/gifcam`


---


## Pi Zero W WiFi and SSH on first boot
These instructions will work for Raspberry Pis that have WiFi on-board eg. Pi 3 B, Zero W.
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
