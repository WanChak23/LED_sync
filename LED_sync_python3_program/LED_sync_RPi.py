import socket
import json
from rpi_ws281x import *
import sys

def colour_brightness(c):
    return Color(c[0],c[1],c[2])


LED_COUNT1 = 60 #number of LEDs
LED_PIN1 = 21 #pin number

LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL0 = 0


TCP_IP = "RPi address here"
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #set up socket
s.bind((TCP_IP,TCP_PORT))
s.listen(1)

strip1 = Adafruit_NeoPixel(LED_COUNT1, LED_PIN1, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL0) #set up LED light strip

strip1.begin()

conn, addr = s.accept() #start receiving data from socket

while True:
    lst2 = []
    data = ""
    
    data = conn.recv(BUFFER_SIZE)
    data = data.decode()
    
    start = time.time()
    
    lst = data.split(";") #Split data into list
    
    i = 0
    for a in lst:
        RGB = a.split(" ") #separate data into list of RGB 
        
        strip1.setPixelColor(i,Color(int(RGB[0]),int(RGB[1]),int(RGB[2])))
        strip1.show()
        
        i += 1 

