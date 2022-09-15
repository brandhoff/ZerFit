# -*- coding: utf-8 -*-
"""

@author: hi84qur
"""

import IDSCam
import numpy as np
from matplotlib.patches import Circle
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
        
    def drawAreaOfInterest(self, axis):
        circ = Circle(self.center,self.radius, fill = True, color = 'pink', alpha = 0.6)
        axis.add_patch(circ)


    def cutImageToAreaOfInterest(self, img):
        return img