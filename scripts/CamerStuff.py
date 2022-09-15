# -*- coding: utf-8 -*-
"""

@author: Jonas
"""
import Tester
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

Cam = Tester.IdsCamera()
Cam.connect()
print(Cam.error_str)

Cam.set_camera_exposure(100000)

img = Cam.grab_image()
print(len(img))


ax1 = plt.subplot()

#create two image plots
im1 = ax1.imshow(img)

def update(i):
    img = Cam.grab_image()

    im1 = ax1.imshow(img)

    
ani = FuncAnimation(plt.gcf(), update, interval=2000)


def close(event):
    if event.key == 'q':
        plt.close(event.canvas.figure)
        Cam.disconnect()

cid = plt.gcf().canvas.mpl_connect("key_press_event", close)

plt.show()

#Cam.disconnect()
