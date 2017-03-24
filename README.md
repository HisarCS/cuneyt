# cuneyt
This Readme will be updated in the near future, 
meanwhile you can refer to comments in the library functions as reference.

Here are instructions on how to install the complete cuneyt system:

## Setup your Raspberry Pi to use with cuneyt
The Cuneyt installation depends on the i2c and camera modules on your Raspberry Pi. To use the cuneyt installer, you must enable i2c and camera interfaces and increase your GPU memmory allocation to 256mB. 
Here is a brief guide on how to do this:
* open a new terminal window `ctr+alt+t`
* run the command `sudo raspi-config` to open the configuration panel
* navigate to `Interfacing Options` with your keyboard
* select `Camera`, navigate to `<Yes>` and click enter
* go to `Interfacing Options` again and do the same steps for i2c
* last, go to `Advanced Options`, `Memory Split` and replace the value you see (128 by default) with `256`
* accept changes and exit the configuration tool
If you complete all the steps above successfully, you will have a Raspberry Pi setup for the Cuneyt Installation. 

## Installation
Cuneyt has a really simple installation script, install.sh, that sets up your Raspberry Pi system with the complete Cuenyt system and dependencies. 
You will need a Raspberry Pi 3 (or older Raspberry Pi models with Internet Connection) with Raspbian installed. For more information on how to do this visit: [The Raspberry Pi Noobs Webpage](https://www.raspberrypi.org/downloads/noobs)
Once you have a Raspberry Pi with Raspian:
* download install.sh
* move install.sh to the directory you want to work in (e.g. Desktop)
* navigate to said directory from your terminal
* run the command `sudo bash install.sh`
* Confirm when the installer asks you to do so
* After setup is complete run `python` and `import cuneyt` to check installation
