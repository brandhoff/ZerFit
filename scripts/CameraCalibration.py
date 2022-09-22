# -*- coding: utf-8 -*-
"""

@author: hi84qur
"""

import IDSCam
import numpy as np
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle

import matplotlib.pyplot as plt


class Camera:
    def __init__(self):
        self.IdsCamera = IDSCam.IdsCamera()
        self.width = 1280
        self.height = 1024
        self.center = (int(self.width / 2), int(self.height/2))
        self.radius = 50
    def connectCamera(self):
        self.IdsCamera.connect()
        if not self.IdsCamera.ok:
            return False
        return True
        
    def disconnectCamera(self):
        self.IdsCamera.disconnect()
        
    def takeFullSizeImage(self):
        img = self.IdsCamera.grab_image()
        return img
    
    def changeExposure(self, intTime):
        self.IdsCamera.set_camera_exposure(intTime)



    def setAreaOfInterest(self, x, y, radius):
        self.center = (x,y)
        self.radius = radius
        
    def drawAreaOfInterest(self, axis, circle = False):
        if circle:
            circ = Circle(self.center,self.radius, fill = True, color = 'pink', alpha = 0.6)
            axis.add_patch(circ)
        else:
            #xy, width, height
            x = self.center[0]- self.radius
            y = self.center[1]- self.radius

            rect = Rectangle((x,y),2*self.radius,2*self.radius, fill = True, color = 'pink', alpha = 0.6)
            axis.add_patch(rect)
        

    def cutImageToAreaOfInterest(self, img):
        x = self.center[0]
        y = self.center[1]
        #reshaped = img.reshape(self.width,self.height)
        cutImg = img[y-self.radius: y+self.radius, x-self.radius : x + self.radius]
        #das macht dass das Bild zurecht geschnitten wird. xy sind hierbei die pixel nummern
        #also center minus radius ist y rand bis y + radius und das geleiche fuer x
        return cutImg