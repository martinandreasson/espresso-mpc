espresso-mpc
============

A Raspberry Pi modification to the Rancilio Silvia Espresso Machine implementing model predictive temperature control.

Features:
---------
* Brew and steam temperature control
* Web interface for displaying temperature and other statistics
* Programmable machine on/off timer and temperature set-point

Hardware
---------
* Raspberry Pi zero W  
  * £10 - https://thepihut.com/collections/raspberry-pi-zero/products/raspberry-pi-zero-w
* GPIO Headers
  * £1 - https://thepihut.com/products/40-pin-2x20-hat-dual-male-headers?variant=21454749700
* Power Adapter
  * £5 - https://thepihut.com/collections/raspberry-pi-power-supplies/products/eu-micro-usb-power-supply-for-the-raspberry-pi
* Micro SD Card
  * £6 - https://thepihut.com/collections/raspberry-pi-sd-cards-and-adapters/products/pimame-preinstalled-sd-card?variant=305692867
* Solid State Relay - For switching on and off the heating element
  * $10 - https://www.sparkfun.com/products/13015
* Thermocouple Amplifier - For interfacing between the Raspberry Pi and Thermocouple temperature probe
  * $15 - https://www.sparkfun.com/products/13266
* Type K Thermocouple - For accurate temperature measurement
  * $15 - http://www.auberins.com/index.php?main_page=product_info&cPath=20_3&products_id=307
* Jumper Cables - For connecting everything together
  * £5 - https://thepihut.com/products/adafruit-premium-female-female-jumper-wires-20-x-12-300mm?ref=isp_rel_prd&isp_ref_pos=3
* 14 gauge wire - For connecting the A/C side of the relay to the circuit
  * $5 - Hardware Store / Scrap

Software
---------
* OS - Raspbian Jessie
  * Lite (no need for a GUI) - https://downloads.raspberrypi.org/raspbian_lite_latest

Install Raspbian and configure Wi-Fi and timezone.

Installation Instructions
--------------------------
Execute on the pi bash shell:
````
sudo apt-get -y update
sudo apt-get -y upgrade
sudo rpi-update
sudo bash -c 'echo "dtparam=spi=on" >> /boot/config.txt'
sudo reboot
````

After reboot
--------------
````
sudo git clone https://github.com/martinandreasson/espresso-mpc.git /root/espresso-mpc
sudo /root/espresso-mpc/setup.sh
````
This last step will download the necessariy python libraries and install the espresso-mpc software in /root/espresso-mpc

It also creates an entry in /etc/rc.local to start the software on every boot.
