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
from skimage.feature import peak_local_max

import numpy as np
from skimage.io import imread
import scipy
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib
import matplotlib as mpl
import matplotlib.colors as colors
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import scipy.ndimage.filters as filters
from collections import OrderedDict
import fitFunctions as FF
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from lmfit.models import Gaussian2dModel
from lmfit import Model, Parameters

import lmfit
from lmfit.lineshapes import gaussian2d, lorentzian
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
        self.ax2 = self.plotSensor_2.canvas.ax
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
        neighborhood_size = 5
        threshold = 1500
        print("TEST Image")

        img = mpimg.imread('testIMG.jpg')
        image = np.zeros((1000, 1000))
        for i in range(len(img)):
            for j in range(len(img)):
                image[i,j] = np.sum(img[i,j])
        self.ax1.imshow(image, cmap = self.colormap)
        self.draw()
        
        self.nFoci = 25
        self.guessList = []
        xy = peak_local_max(image,threshold_abs= 0, min_distance=int((len(img))/self.nFoci-10))
        #image_max = ndimage.maximum_filter(image, size=10, mode='constant')
        #self.ax2.imshow(image_max, cmap = self.colormap)


        for t in xy:
            self.ax1.plot(t[1], t[0], 'o', color='orange')
            self.guessList.append(t)
            #self.fitLM2DGaussian(image, t[1], t[0], image[t[1],t[0]])
            #self.fit2DGaussian(image, t[1], t[0], image[t[1],t[0]])
        self.draw()
        self.buildAnalyticGrid(image, 25)
        
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
    def fit2DGaussian(self, image, x0, y0, ampl):
        """
        This functions fits a 2D Gaussian (defined in fitFunctions) to a spot at init guess x0 y0 with ampl
        as amplitdue nad draws the contour

        Parameters
        ----------
        image : ndarray
            The image.
        x0 : int
            init x guess.
        y0 : TYPE
            init y guess.
        ampl : TYPE
            init ampl guess.

        Returns
        -------
        None.

        """
        x = np.linspace(0, len(image[0,:]), len(image[0,:]))
        y = np.linspace(0, len(image[:,0]), len(image[:,0]))
        x, y = np.meshgrid(x, y)
        initial_guess = (ampl, x0, y0, 1, 1, 0, 0)
        popt, pcov = opt.curve_fit(FF.twoD_Gaussian, (x, y), image.ravel(), p0=initial_guess,maxfev = 200)#5600
        data_fitted = FF.twoD_Gaussian((x, y), *popt)
        self.ax1.contour(x, y, data_fitted.reshape(len(image[0,:]), len(image[:,0])), 8, colors='w')


    def fitLM2DGaussian(self, image, x0, y0, ampl, threshHold = 10):
        """
        this function utilieses the LMFit libary for a percise fit
        

        Parameters
        ----------
        image : TYPE
            DESCRIPTION.
        x0 : TYPE
            DESCRIPTION.
        y0 : TYPE
            DESCRIPTION.
        ampl : TYPE
            DESCRIPTION.
        threshHold : TYPE, optional
            DESCRIPTION. The default is 10.

        Returns
        -------
        None.

        """
        x = np.linspace(0, len(image[0,:]), len(image[0,:]))
        y = np.linspace(0, len(image[:,0]), len(image[:,0]))
        x, y = np.meshgrid(x, y)
        fit_model = Gaussian2dModel(prefix='peak_')
        params = Parameters()
        params.add_many(
            ('peak_'+'amplitude', ampl, True, 0, 1000),
            ('peak_'+'centerx', x0, True, x0-threshHold, x0+threshHold),
            ('peak_'+'centery', y0, True, y0-threshHold, y0+threshHold),
            ('peak_'+'sigmax', 0.25, True, 0, 1),
            ('peak_'+'sigmay', 0.25, True, 0, 1)

            )
        result = fit_model.fit(image, params, x=x, y=y)
        self.ax1.contour(x, y, result.best_fit, 3, colors='w')




#Grid Functions



    def buildAnalyticGrid(self, image, numFoci):
        imageWidth = len(image[:,0])
        imageHeight = len(image[0,:])
        print(imageWidth)
        print(imageHeight)






#Functions for the canvas for clearing etc.


    def draw(self):
        self.plotSensor.canvas.draw()
        self.plotSensor_2.canvas.draw()
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