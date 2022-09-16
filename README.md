# LED_sync
This is a DIY AmbiLight project with a RaspberryPi for MacOS.
LED light strips are installed at the back of the monitor.
The colour of every single LED shows different colour according to the colour change on the screen.
The light strips extremely enhance the experience of watching movie. 



In this project, the code will be slpitted into two parts.
The first part captures the screen of Mac, progresses the data and send to the RaspberryPi through WiFi by TCP socket.
The second part receives the data and sets the colour of the LED strip according to the data.
