# -*- coding: utf-8 -*-
"""

@author: Jonas
"""
import Tester
import matplotlib.pyplot as plt

Cam = Tester.IdsCamera()
Cam.connect()
print(Cam.error_str)
img = Cam.grab_image()
print(len(img))
plt.imshow(img)

#Cam.disconnect()
