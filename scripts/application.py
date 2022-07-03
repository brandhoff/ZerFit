# -*- coding: utf-8 -*-
"""
Created on Sun Jul 03 11:14:09 2022

@author: Jonas Brandhoff
for Friedrich Schiller Universität Jena
"""

import os
import sys

import scipy.optimize as opt
import random
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFileDialog

from MainWindow import Ui_MainWindow

import numpy as np
from skimage.io import imread

from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib
import matplotlib as mpl
import matplotlib.colors as colors
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from collections import OrderedDict
import fitFunctions as FF
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')






class Window(QMainWindow, Ui_MainWindow):
    """
    This is the Main class Loading the window created in the pyqt Designer
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        colorlist=["#001f78","#3d66d9","#53b4c9","#2adea2","#8ccf55", "#eded1f", "#c49110", "#d41f0f"]
        self.colormap = LinearSegmentedColormap.from_list('testCmap', colors=colorlist, N=1000)
        self.ax1 = self.plotSensor.canvas.ax

    def connectSignalsSlots(self):
        """
        This connects the button Presses etc with the corresponding action functions
        """
        self.btnTakeImage.clicked.connect(self.TestImageProcessing)
        self.btnShow.clicked.connect(self.reconstructWavefront)


#Action Functions

    def TestImageProcessing(self):
        """
        This function is used for testing on an artificial image

        Returns
        -------
        None.

        """
        print("TEST Image")

        img = mpimg.imread('testIMG.jpg')
        image = np.zeros((1000, 1000))
        for i in range(len(img)):
            for j in range(len(img)):
                image[i,j] = np.mean(img[i,j])
        self.ax1.imshow(image, cmap = self.colormap)
        self.draw()
        
        
        self.guessList = []
        self.nFoci = 25
        
        for i in range(self.nFoci):
            self.fit2DGaussian(image, 0, 0)

        
        self.draw()
        
    def takeImage(self):
        """
        Fired when the take image button is pressed will take an Image of the sensor
        and will display it in the left Canvas

        Returns
        -------
        None.

        """
        print("taking Image")

    def reconstructWavefront(self):
        """
        Reconstructs the wavefront and plots it

        Returns
        -------
        None.

        """
        print("reconstructing Wavefront")




#Spot fitting fucntions:
    def fit2DGaussian(self, image, x0, y0):

        x = np.linspace(0, len(image[0,:]), len(image[0,:]))
        y = np.linspace(0, len(image[:,0]), len(image[:,0]))
        x, y = np.meshgrid(x, y)
        initial_guess = (50, x0, y0, 1, 1, 0, 0)
        popt, pcov = opt.curve_fit(FF.twoD_Gaussian, (x, y), image.ravel(), p0=initial_guess,maxfev = 200)#5600
        data_fitted = FF.twoD_Gaussian((x, y), *popt)
        self.ax1.contour(x, y, data_fitted.reshape(len(image[0,:]), len(image[:,0])), 8, colors='w')














#Functions for the canvas for clearing etc.


    def draw(self):
        self.plotSensor.canvas.draw()

    def plotClear(self):
        self.plotSensor.canvas.ax.cla()
        self.plotSensor.canvas.draw()
        
        



    def save(self):
        self.plotSensor.canvas.fig.savefig("Figure.pdf");


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    win = Window()
    win.show()
    sys.exit(app.exec())