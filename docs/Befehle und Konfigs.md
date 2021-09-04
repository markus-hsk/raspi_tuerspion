## Browser im Kioskmode starten
	$ sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart

## Kameramodul restarten
	$ sudo service motion restart

## CronJobs
	$ sudo crontab -e
	
	# Motion log löschen beim Bootvorgang und nach jeder Stunde aber dann zur ersten Minute
	@reboot /usr/bin/sudo /bin/rm /var/log/motion/motion.log
	1 * * * * /usr/bin/sudo /bin/rm /var/log/motion/motion.log

	#@reboot /usr/bin/sudo /bin/chmod 777 /sys/class/backlight/rpi_backlight/bl_pow$
	#@reboot /usr/bin/sudo /usr/bin/python3 /home/pi/Dev/raspi_tuerspion/src/displa$

	# Kameraservice alle 15 Minuten neustarten um das Kamerabild neu zu justieren
	*/15 * * * * /usr/bin/sudo service motion restart

