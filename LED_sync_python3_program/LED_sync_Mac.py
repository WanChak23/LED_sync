#!/usr/bin/env python
# coding: utf-8

# In[5]:


from mss import mss
import numpy as np
import socket
from PIL import Image

""" Set up """
sct = mss()

scn_w = 2560     #screen_width
scn_h = 1440     #screen_height
num_LED_w = 17     #number of horizontal LED 
num_LED_h = 13      #number of vertical LED
    
w_crop = 20         #capture size height
h_crop = 20         #capture size width
h_r_scn = (scn_h - (2*w_crop))    #real capture screen height

w = (scn_w/num_LED_w)+1     #number of pixels to capture in width


top_shift = 200

if type(w) == float:

    w = int(w)
    while ((w*num_LED_w-scn_w) <0):
        w +=1 
               
h = (h_r_scn/num_LED_h)+1            #number of pixels to capture in width

if type(h) == float:
    h = int(h)
    while (h*num_LED_h-h_r_scn) <0:
        
        h+=-1
        
h_top = w_crop
shape_w =w*w_crop*4
shape_h =h*h_crop*4

w_bottom = scn_h- w_crop
h_rhs = scn_w - h_crop  


TCP_IP1 = "RPi ip address here "
TCP_PORT1 = 5005
BUFFER_SIZE = 1024
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((TCP_IP1, TCP_PORT1))



"""functions"""
def grab_c(top, left, width, height,shape):
    mon = {'top': top, 'left':left,'width': width,'height':height}
    sct_img = sct.grab(mon)
    
    img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)

    npimg = np.array(img)

    npimg_reshape = np.reshape(npimg.flatten(),(shape,3))
    out_c = np.quantile(npimg_reshape,0.75, axis=0)
    out_c = out_c.astype(int)
    

    return out_c.tolist()

def t_grab(start,end,num,top, width, height,shape):
    for i in range(start,end,num):
        lst.append(grab_c(top, i, width, height,shape))
def b_grab(start,end,num,top, width, height,shape):
    for i in range(start,end,num):
        lst.append(grab_c(top, i, width, height,shape))
        
def r_grab(start,end,num,left, width, height,shape):
    for i in range(start,end,num):
        lst.append(grab_c(i, left, width, height,shape))

def l_grab(start,end,num,left, width, height,shape):
    for i in range(start,end,num):
        lst.append(grab_c(i, left, width, height,shape))

def lst_data(lst):
    return (str(lst).replace("[[","").replace("]]","").replace("], [",";").replace(",", "")).encode()

""" main """

while True:

    lst = []
    lst1 = []

    t_grab(0,scn_w,w,top_shift,w,w_crop,shape_w) #grab the colour from the top
    r_grab(h_top,h_r_scn,h,h_rhs,h_crop,h,shape_h)#grab the colour from the right side  
    b_grab(0,scn_w,w,w_bottom-top_shift,w,w_crop,shape_w) #grab the colour from the bottom
    l_grab(h_top,h_r_scn,h,0,h_crop,h,shape_h) #grab the colour from the left side
    
    lst1 = lst    
    lst1.append(lst1.pop(0))

    s1.send(lst_data(lst1))

#end

