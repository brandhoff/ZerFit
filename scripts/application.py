# -*- coding: utf-8 -*-
"""
Created on Sun Jul 03 11:14:09 2022

@author: Jonas Brandhoff
for Friedrich Schiller Universität Jena
"""

import os
import sys
import math
import scipy.optimize as opt
from scipy import ndimage as ndi
import random
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QMenu
)
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFileDialog

from MainWindow import Ui_MainWindow
from skimage.feature import peak_local_max

import numpy as np
from skimage.io import imread
import scipy as sp
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
import Grid
import CameraCalibration
import lmfit
from PyQt5.QtWidgets import (QApplication, QFileDialog, QWidget)
from PyQt5 import QtGui
from PyQt5.QtCore import QEvent
import zernike
import fast_zernike
from lmfit.lineshapes import gaussian2d, lorentzian
# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

class DummySaveFileDialogWidget(QWidget):

    def __init__(self, title="Save Graph", filters="PDF File (*.pdf)"):
        super().__init__()
        self.title = title
        self.filters = filters
        self.fname = self.savefiledialog()

    def savefiledialog(self):
        filename, _ = QFileDialog.getSaveFileName(caption=self.title,
                                                  filter=self.filters)
        return filename


class TXTSaveFileDialogWidget(QWidget):

    def __init__(self, title="Save FitResult", filters="Txt File (*.txt)"):
        super().__init__()
        self.title = title
        self.filters = filters
        self.fname = self.savefiledialog()

    def savefiledialog(self):
        filename, _ = QFileDialog.getSaveFileName(caption=self.title,
                                                  filter=self.filters)
        return filename



#TODO list:
    #Es muss unbedingt ein weg gefunden werden das analytsiche grid richtig zu centern
    #dafuer muss man halt wissen wo genau das eigentlich center ist -> mit den pfeilen shiften bis es passt?
    #
    #Eine kreis maske einfuegen
    #
    #Eventuell einen bool knopf fuer halt 2D gauss fitten
    #
    #ich bin gespannt wie gross der spot des lasers dann ist...
    #
    #na mal sehen

class Window(QMainWindow, Ui_MainWindow):
    """
    This is the Main class Loading the window created in the pyqt Designer
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle("ZerFit")
        self.setupUi(self)
        self.connectSignalsSlots()

        colorlist=["#001f78","#3d66d9","#53b4c9","#2adea2","#8ccf55", "#eded1f", "#c49110", "#d41f0f"]
        self.colormap = LinearSegmentedColormap.from_list('testCmap', colors=colorlist, N=1000)
        self.ax1 = self.plotSensor.canvas.ax
        self.ax2 = self.plotSensor_2.canvas.ax
        self.axAnalyse = self.plotAnalyse.canvas.ax
        self.axCali = self.plotSensor_3.canvas.ax

        self.grid = []
        self.nFoci = 64 #default
        self.relativeShifts = []
        self.guessList = []
        self.AnylseArr = []
        self.calcCoeff = []
        
        #CAMER Stuff
        self.caliImg = []
        self.Camera = CameraCalibration.Camera()
        self.isConnected = False
        self.caliImg = None
        self.sliderCaliRadius.setProperty("maximum", 500)

    def connectSignalsSlots(self):
        """
        This connects the button Presses etc with the corresponding action functions
        """
        self.btnTakeImage.clicked.connect(self.TestImageProcessing)
        self.btnShow.clicked.connect(self.reconstructWavefront)
        self.btnSavePDF.clicked.connect(self.save)
        
        #slider
        self.horizontalSlider.valueChanged.connect(self.updateWav)
        self.sliderAnalyse.valueChanged.connect(self.updateAnalyseView)

        
        self.btnCreateGrid.clicked.connect(self.buildGrid)
        
        
        #self.btnFindSpots.clicked.connect(self.findSpotInGrid_singleCell)
        
        self.btnFindSpots.clicked.connect(self.findSpotInGridUsingGaussian)
        
        self.btnSave_2.clicked.connect(self.saveRAW)
        
        
        #ANALYSE
        self.btnPlotZernike.clicked.connect(self.showSingleZernike)
        
        self.btnFindSpotsCali.clicked.connect(self.loadTXT)#load already obtained data
        self.plotSensor_2.installEventFilter(self)#right click menu event filter
        self.plotSensor.installEventFilter(self)#right click menu event filter
        self.plotAnalyse.installEventFilter(self)
        
        #Camera Cali
        #self.plotSensor_3.installEventFilter(self)#right click menu event filter
        
        self.idCallCanvas = self.plotSensor_3.canvas.mpl_connect('button_press_event', self.CaliImgClick)
        self.btnCaliConnect_2.clicked.connect(self.takeCaliImage) #TODO ändere diesen var namen
        self.btnCaliConnect.clicked.connect(self.clickConnect)
        self.btnCaliDisconnect.clicked.connect(self.clickDisconnect)
        self.btnCaliRadius.clicked.connect(self.clickSetRadius)#TODO der kann raus
        

#Action Functions

    def TestImageProcessing(self):
        """
        This function is used for testing on an artificial image

        Returns
        -------
        None.

        """
        self.plotSensor.canvas.ax.cla()
        self.plotSensor_2.canvas.ax.cla()
        print("TEST Image")

        #img = mpimg.imread('may.jpg')

        #image = np.zeros((1000, 1000))
        #for i in range(len(img)):
        #    for j in range(len(img)):
        #        image[i,j] = np.mean(img[i,j])
        
        image = self.cutImg
        self.ax1.imshow(image, cmap = self.colormap)
       

        self.nFoci = self.gridGuess#64#len(xy)
        print(self.nFoci)
        self.image = image
        self.imageHeighth = len(image[:,0])
        self.imageWidth = len(image[0,:])
        
        self.ax1.set_xlim(0, self.imageWidth-1)
        self.ax1.set_ylim(0, self.imageHeighth-1)
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
        
        #self.calculateRelativeShifts()
        order = self.spinBox.value()
        
        
        coefficients = self.fit_wavefront(n_zernike=order)
        self.calcCoeff = coefficients

        wavefront = zernike.Wavefront(coefficients=coefficients)     
        x_0, y_0 = zernike.get_unit_disk_meshgrid(resolution=1000)
        wf_grid = zernike.eval_cartesian(wavefront.cartesian, x_0=x_0, y_0=y_0)
    
        """

        """
        maximum = self.horizontalSlider.value() / 1000
        wf_grid[np.isnan(wf_grid)] = -1 
        self.calculatedWavGrid = wf_grid
        self.ax2.imshow(wf_grid, interpolation='nearest', cmap=self.colormap,
                        vmin=-maximum, vmax=maximum)
        
        #self.ax2.set_xlim(0, self.imageWidth)
        #self.ax2.set_ylim(0, self.imageHeight)
        self.draw()

    def updateWav(self):
        if self.calculatedWavGrid is None:
            return
        else:
            self.ax2.cla()
            maximum = self.horizontalSlider.value() / 1000
        
            self.ax2.imshow(self.calculatedWavGrid, interpolation='nearest', cmap=self.colormap,
                        vmin=-maximum, vmax=maximum)
            #self.ax2.set_xlim(0, self.imageWidth)
            #self.ax2.set_ylim(0, self.imageHeight)
            self.plotSensor_2.canvas.draw()






    def buildGrid(self, axis = None):
        """
        

        Returns
        -------
        None.

        """
        print(self.nFoci)

        self.buildAnalyticGrid(self.image, self.nFoci)
        self.drawGrid(axis = axis)
        self.draw()






    def findSpotInGrid(self):
        """
        Finds all spots, does not look inside a cell but associates a cell with a found spot

        Returns
        -------
        None.

        """
        self.relativeShifts = []
        flagZeros = False
        flagMultiple = False

        for cell in self.grid:
            img = self.image
            lowerleft = cell.relToAb((-1,-1)) #unten links
            upperright = cell.relToAb((1,1))#oben rechts
            #sliecedCell = img[int(lowerleft[0]):int(upperright[0]), int(lowerleft[1]):int(upperright[1])]
            
            #xy = peak_local_max(sliecedCell,min_distance = 20, exclude_border = 0, num_peaks=1)
            xy = self.fociGuess
            if len(xy) == 1:
                item = xy[0]
                abItemX = item[0]# + lowerleft[0]
                abItemY = item[1]# + lowerleft[1]
                
                (relItemX, relItemY) = cell.abToRel((abItemX,abItemY))

                self.relativeShifts.append((relItemX, relItemY))
                self.ax1.plot(abItemX, abItemY, 'o', color='orange', alpha=0.5)
            elif len(xy) == 0:
                flagZeros = True
                self.relativeShifts.append((0, 0))
            else:
                item = xy[0]
                abItemX = item[0] + lowerleft[0]
                abItemY = item[1] + lowerleft[1]
                
                (relItemX, relItemY) = cell.abToRel((abItemX,abItemY))

                self.relativeShifts.append((relItemX, relItemY))
                self.ax1.plot(abItemX, abItemY, 'o', color='green', alpha=0.7)
                flagMultiple = True

                
        self.draw()
        if flagZeros:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("No Spot Found")
                msg.setInformativeText('While trying to find a Spot inside a cell nothing was found! Maybe the wavefront is too curved. If this was intended the code will proceed as rel. shift of 0!')
                msg.setWindowTitle("Error")
                msg.exec_()
        if flagMultiple:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("Many Spots Found")
                        msg.setInformativeText('While trying to find a Spot inside a cell multiple were found! Maybe the wavefront is too curved. If this was intended the code will proceed as if the first guess was the best!')
                        msg.setWindowTitle("Error")
                        msg.exec_()












    def findSpotInGridUsingGaussian(self):
        """
        Trys to Fit a 2D Gaussian for each build cell

        Returns
        -------
        None.

        """
        self.relativeShifts = []
        for cell in self.grid:
            img = self.image
            lowerleft = cell.relToAb((-1,-1)) #unten links
            upperright = cell.relToAb((1,1))#oben rechts
            sliecedCell = img[int(lowerleft[0]):int(upperright[0]), int(lowerleft[1]):int(upperright[1])]
              
            #Die foci guesses als init guess der gaussfunktionen nehmen:
            globalGuess = self.fociGuess
            x0 = 0
            y0 = 0
            for item in globalGuess:
                self.ax1.plot(item[1], item[0], 'x', color='green')
                if cell.isInside(item):
                    x0 = item[1]
                    y0 = item[0]
                    break
                    #print("jup inside :D")
           # 
            result, mesh = self.fitLM2DGaussian(img, x0 = x0, y0 = y0)
            
            x = mesh[0]
            y = mesh[1]
            report = lmfit.fit_report(result.params)
            py = result.params['peak_centerx'].value
            px = result.params['peak_centery'].value
            print(px)
            print(py)
            (relItemX, relItemY) = cell.abToRel((px,py))
            print(relItemX)
            self.relativeShifts.append((relItemX, relItemY))
            self.ax1.contour(x, y, result.best_fit,  colors='black')
            self.draw()


    def findSpotInGrid_singleCell(self):
        """
        Finds all spots for all cells, looks only for spots inside of each cell

        Returns
        -------
        None.

        """
        self.relativeShifts = []
        flagZeros = False
        flagMultiple = False

        for cell in self.grid:
            img = self.image
            lowerleft = cell.relToAb((-1,-1)) #unten links
            upperright = cell.relToAb((1,1))#oben rechts
            sliecedCell = img[int(lowerleft[0]):int(upperright[0]), int(lowerleft[1]):int(upperright[1])]
            
            xy = peak_local_max(sliecedCell)#,min_distance = 1, num_peaks=1)
           
            if len(xy) == 1:
                item = xy[0]
                abItemX = item[0] + lowerleft[0]
                abItemY = item[1] + lowerleft[1]
                
                (relItemX, relItemY) = cell.abToRel((abItemX,abItemY))

                self.relativeShifts.append((relItemX, relItemY))
                self.ax1.plot(abItemX, abItemY, 'o', color='orange', alpha=0.5)
            elif len(xy) == 0:
                flagZeros = True
                self.relativeShifts.append((0, 0))
            else:
                item = xy[0]
                abItemX = item[0] + lowerleft[0]
                abItemY = item[1] + lowerleft[1]
                
                (relItemX, relItemY) = cell.abToRel((abItemX,abItemY))

                self.relativeShifts.append((relItemX, relItemY))
                self.ax1.plot(abItemX, abItemY, 'o', color='green', alpha=0.7)
                flagMultiple = True

                
        self.draw()
        if flagZeros:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("No Spot Found")
                msg.setInformativeText('While trying to find a Spot inside a cell nothing was found! Maybe the wavefront is too curved. If this was intended the code will proceed as rel. shift of 0!')
                msg.setWindowTitle("Error")
                msg.exec_()
        if flagMultiple:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("Many Spots Found")
                        msg.setInformativeText('While trying to find a Spot inside a cell multiple were found! Maybe the wavefront is too curved. If this was intended the code will proceed as if the first guess was the best!')
                        msg.setWindowTitle("Error")
                        msg.exec_()


    def createGallery(self):
        
        self.findSpotInGrid()





    def eventFilter(self, source, event):
        #RIGHT CLICK MENU FOR THE WAVE FRONT
        if event.type() == QEvent.ContextMenu and source is self.plotSensor_2:
            menu = QMenu()
            acShow3D = menu.addAction('Show 3D')
            acShowCoeff = menu.addAction('Show Coefficients')
            action = menu.exec_(event.globalPos())
            if action == acShow3D:
                print("Showing now 3D")
                if len(self.calculatedWavGrid) > 0:
                    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
                    x_0, y_0 = zernike.get_unit_disk_meshgrid(resolution=1000)
                    limit = np.nanmax(np.abs(self.calculatedWavGrid))
                    surf = ax.plot_surface(x_0, y_0, self.calculatedWavGrid, cmap=self.colormap, linewidth=0, antialiased=False)
                    maxi = np.amax(self.calculatedWavGrid)
                    mini = np.amin(self.calculatedWavGrid)
                    ax.set_zlim(mini, maxi)
                return True
            if action == acShowCoeff:
                print("Showing Coeffs")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Coefficients")
                stringShow = ''
                for i,coeff in enumerate(self.calcCoeff):
                    stringShow+='j='+str(i)+': '+str(coeff)+ '\n'
                msg.setInformativeText(stringShow)
                msg.setWindowTitle("Coefficients")
                msg.exec_()

        
        #RIGHT CLICK MENU FOR THE IMAGE

        if event.type() == QEvent.ContextMenu and source is self.plotSensor:
            menu = QMenu()
            acHideGrid = menu.addAction('Hide Grid')
            acFindSpots = menu.addAction('Find Spots')
            action = menu.exec_(event.globalPos())
            if action == acHideGrid:
                print("Hide Grid")
                self.ax1.cla()                
                self.ax1.imshow(self.image, cmap = self.colormap)
                self.ax1.set_xlim(0, len(self.image[0,:]))
                self.ax1.set_ylim(0, len(self.image[:,0]))
                self.draw()
            if action == acFindSpots:
                self.findSpotInGrid()
            return True
        
        #RIGHT CLICK MENU FOR ANALYSIS

        if event.type() == QEvent.ContextMenu and source is self.plotAnalyse:
            menu = QMenu()
            acShowPoly = menu.addAction('Show Polynom')
            action = menu.exec_(event.globalPos())
            if action == acShowPoly:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Polynom of Degree: " + str(self.spinBoxSingleZernike.value()))
                stringShow = 'Cartesian:' + '\n' + str(zernike.ZernikePolynomial(j=self.spinBoxSingleZernike.value()).cartesian) +'\n' + 'Polar:' + '\n' + str(zernike.ZernikePolynomial(j=self.spinBoxSingleZernike.value()).polar)
                msg.setInformativeText(stringShow)
                msg.setWindowTitle("Polynom")
                msg.exec_()

            return True
        
        if event.type() == QEvent.ContextMenu and source is self.plotSensor_3:
            print(event.x())
            
            return True
        
        
        return super().eventFilter(source, event)
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#--------------------------CAMERA Calibration-----------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

    def CaliImgClick(self, click):
        #print(click.xdata)
        if len(self.deepCopyImg) > 0:
            self.axCali.cla()
            self.axCali.imshow(self.deepCopyImg, cmap = self.colormap)
            radius = self.sliderCaliRadius.value()
            self.Camera.setAreaOfInterest(int(click.xdata), int(click.ydata), radius)
            self.Camera.drawAreaOfInterest(self.axCali)
            self.axCali.set_xlim(0, len(self.deepCopyImg[0,:])-1)
            self.axCali.set_ylim(0,len(self.deepCopyImg[:,0])-1)
            self.draw()
    def clickConnect(self):
        if self.Camera.connectCamera():
            self.connected = True

    def clickDisconnect(self):
        if self.connected:
            self.Camera.disconnectCamera()

    def takeCaliImage(self):
        if self.connected:
            self.axCali.cla()
            img = self.Camera.takeFullSizeImage()
            self.caliImg = img
            self.deepCopyImg = img.copy()
            self.axCali.imshow(img, cmap = self.colormap)
            self.axCali.set_xlim(0, len(img[0,:])-1)
            self.axCali.set_ylim(0,len(img[:,0])-1)
            self.draw()

    def clickSetRadius(self):#TODO das kann spaeter alles raus
        self.axCali.cla()
        cutImg = self.Camera.cutImageToAreaOfInterest(self.deepCopyImg)
        self.axCali.imshow(cutImg, cmap = self.colormap)
        self.cutImg = cutImg
        self.tellMeAboutFoci(cutImg)
        self.draw()

    def tellMeAboutFoci(self, img):
        
        xy = peak_local_max(img.reshape(2*self.Camera.radius, 2*self.Camera.radius), min_distance = 20, exclude_border = 0)
        
        print("I guessed a grid of size:")
        print(round(np.sqrt(len(xy))))
        self.gridGuess = round(np.sqrt(len(xy)))**2
        self.fociGuess = xy
        image = img
        self.nFoci = self.gridGuess
        print(self.nFoci)
        self.image = image
        self.imageHeight = len(image[:,0])
        self.imageWidth = len(image[0,:])
        
        self.axCali.plot(xy[:,1], xy[:,0], 'x', color='green')

        self.buildGrid(axis = self.axCali)
        self.axCali.set_xlim(0, self.imageWidth-1)
        self.axCali.set_ylim(0,self.imageHeight-1)
















#---------------------------------------------------------------------
#---------------------------------------------------------------------
#--------------------------ANALYSIS-----------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

    def showSingleZernike(self):
        self.axAnalyse.cla()
        x_0, y_0 = zernike.get_unit_disk_meshgrid(resolution=1000)
        wf_grid = zernike.eval_cartesian(zernike.ZernikePolynomial(j=self.spinBoxSingleZernike.value()).cartesian, x_0=x_0, y_0=y_0)
        limit = np.nanmax(np.abs(wf_grid))
        
        self.axAnalyse.imshow(wf_grid,cmap=self.colormap, vmin = -limit,vmax = limit)
        self.draw()




    def loadTXT(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', 
         'c:\\',"RAW file (*.txt)")
        if filename:
            self.axAnalyse.cla()
            readARR = np.loadtxt(filename)
            self.AnylseArr = readARR
            self.axAnalyse.imshow(readARR,cmap=self.colormap) 
            self.axAnalyse.set_xlim(0, len(self.AnylseArr[0]))
            self.axAnalyse.set_ylim(0, len(self.AnylseArr))

            self.draw()


    def updateAnalyseView(self):
        self.axAnalyse.cla()
        maximum = self.sliderAnalyse.value() / 1000
    
        self.axAnalyse.imshow(self.AnylseArr, interpolation='nearest', cmap=self.colormap,
                    vmin=-maximum, vmax=maximum)
        self.axAnalyse.set_xlim(0, len(self.AnylseArr[0]))
        self.axAnalyse.set_ylim(0, len(self.AnylseArr))
        self.plotAnalyse.canvas.draw()


#Spot fitting fucntions:
    
    
    def fit2DGaussian(self, image, x0 = 0, y0 = 0, ampl = 100):
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
        initial_guess = (2, (len(image[0,:]/2)),(len(image[:,0]/2)), (len(image[0,:]/6)), (len(image[0,:]/6)), 0, 0)
        popt, pcov = opt.curve_fit(FF.twoD_Gaussian, (x, y), image.ravel(), p0=initial_guess,maxfev = 200)#5600
        data_fitted = FF.twoD_Gaussian((x, y), *popt)
        #self.ax1.contour(x, y, data_fitted.reshape(len(image[0,:]), len(image[:,0])), 8, colors='black')
        mesh = (x, y)
        return data_fitted, mesh

    def fitLM2DGaussian(self, image,x0 = 0,y0=0, ampl=100, threshHold = 10):
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
        
        
        
        x1 = np.linspace(0, len(image[:,0]), len(image[:,0]))
        y1 = np.linspace(0, len(image[0,:]), len(image[0,:]))
        #print(x1)
        x, y = np.meshgrid(x1, y1)

        #x0 = max(x1) / 2
        #y0 = max(y1) / 2
        fit_model = Gaussian2dModel(prefix='peak_')
        params = Parameters()
        params.add_many(
            ('peak_'+'amplitude', np.amax(image)-1, True, 0, np.amax(image)),
            ('peak_'+'centerx', x0, True, x0-0.1*y0, x0+0.1*x0),
            ('peak_'+'centery', y0, True, y0-0.1*y0, y0+0.1*y0),
            ('peak_'+'sigmax', 2, True, 0, 6))
            #('peak_'+'sigmay', 0.25, True, 0, 1))
        params.add('peak_sigmay', expr='peak_sigmax')

        result = fit_model.fit(image, params, x=x, y=y)
        #print(result)
        mesh = (x,y)
        return result, mesh
        #self.ax1.contour(x, y, result.best_fit, 3, colors='w')




#Grid Functions



    def drawGrid(self, axis = None):
        """
        Draws the Grid of Cells

        Returns
        -------
        None.

        """
        if not axis:
            axis = self.ax1
        for cell in self.grid:
            cell.dotCenter(axis, color = 'red')
            cell.drawRect(axis)
            

    def buildAnalyticGrid(self, image, numFoci):
        """
        Builds an equi distant grid containing n cells where n is the 
        number of foci.

        Parameters
        ----------
        image : 2d array
            the image.
        numFoci : TYPE
            the number of foci used to build the grid.

        Returns
        -------
        None.

        """
        self.grid = []
        numPer = int(np.sqrt(numFoci))
        
        for xi in range(numPer):
            for yi in range(numPer):
                width = self.imageWidth/numPer
                height = self.imageHeight/numPer
                posX = width/2 + xi*width
                posY = height/2 + yi*height
                cell = Grid.Cell((posX,posY),width, height = height)
                self.grid.append(cell)



    def findCellForSpot(self, SpotCoords):
        """
        Finds the cell in which a given pair of coords sits on the grid

        Parameters
        ----------
        SpotCoords : TYPE
            DESCRIPTION.

        Returns
        -------
        cell : Cell
            the cell in which the spot lies.

        """
        if not self.grid[0]:
            print("no grid")
            return
        for cell in self.grid:
            if cell.isInside(SpotCoords):
                return cell



    def toRelImageCoords(self, AbsCoord):
        midX = self.imageWidth/2
        midY = self.imageHeight/2
        xRel = (AbsCoord[0]-midX)/(self.imageWidth/2)
        yRel = (AbsCoord[1]-midY)/(self.imageHeight/2)
        return (xRel,yRel)

    def toAbsImageCoords(self, RelCoord):
        midX = self.imageWidth/2
        midY = self.imageHeight/2
        xAbs = RelCoord[0]*self.imageWidth/2+midX
        yAbs = RelCoord[1]*self.imageHeight/2+midY
        return (xAbs,yAbs)
    
    
#Zernike Functions
    def fit_wavefront(self,n_zernike: int = 9,) -> np.ndarray:
            """
            Perform a modal (i.a. Zernike polynomial-based) least squares
            fit to find the wavefront that matches the sensor data. The
            result is a vector of Zernike coefficients.
            For more details (also about, for example, the notation), please
            see [Cubalchini_1979]_. For an alternative discussion of the
            same topic, see also, for example, section 4.3.2 of [Dai_2007]_.
            .. note::
                Note that the code in this package uses a slightly different
                notation for indexing the Zernike polynomials: when using
                only a single index :math:`j`, we start counting them at
                :math:`j = 0` (the constant polynomial which corresponds to
                :math:`Z^0_0` when using double indices :math:`m` and
                :math:`n`). [Cubalchini_1979]_, on the other hand, starts
                counting the Zernike polynomials at 1, which is clearly
                unpythonic :)
            .. note::
                For compatibility reasons, the coefficient vector that is
                return by the function will also contain a value for the
                first Zernike polynomial :math:`Z^0_0`, which is always set
                to be zero. the coefficient vector will, therefore, have
                `n_zernike + 1` entries.
            .. warning::
                Fitting the wavefront requires the Cartesian derivatives of
                the Zernike polynomials. Computing these "on the fly" is
                relatively slow, which is why there exists the
                :py:mod:`hswfs.fast_zernike` module, which contains
                pre-computed versions of these derivatives up to
                :math:`j = 135`. If `n_zernike` is chosen to be larger than
                this value, fitting the wavefront may take a relatively
                long time. However, for most practical purposes, using this
                many Zernike polynomials will probably be unnecessary.
            Args:
                n_zernike: The number of Zernike polynomials to be used in
                    the fit. Note that :math:`Z^0_0` (the constant term) is
                    ignored in the fit.
                    The index `j_max` of the Zernike polynomial with the
                    highest order will, therefore, be `n_zernike + 1`.
            Returns:
                A numpy array of length `n_zernike + 1`, where the
                :math:`j`-th entry is the coefficient that corresponds to
                the Zernike polynomial :math:`Z_j`.
            """
    
            # ---------------------------------------------------------------------
            # Compute the P vector
            # ---------------------------------------------------------------------
    
            # Shortcut for the total number of apertures in the grid
            n_ap = self.nFoci
    
            # Create p-vector from measured shifts:
            #   (x_shift_1, x_shift_2, ..., x_shift_N, y_shift_1,  ..., y_shift_n)
            #p = np.concatenate((self.relative_shifts[:, :, 0].reshape(n_ap),self.relative_shifts[:, :, 1].reshape(n_ap)))
            p = []
            for relShift in self.relativeShifts:
                p.append(relShift[0])
                
            for relShift in self.relativeShifts:
                p.append(relShift[1])
            # ---------------------------------------------------------------------
            # Compute the D matrix of derivatives of Zernike polynomials
            # ---------------------------------------------------------------------
    
            # Initialize D.
            # According to eq. (14) in [Cubalchini_1979], D is a matrix of shape:
            #   (n_zernike, 2 * n_subapertures),
            # with entries defined as:
            #   D_ab = \frac{\partial Z_a}{\partial x} (x, y)_b
            #   if 0 < b <= n_subapertures,
            # and
            #   D_ab = \frac{\partial Z_a}{\partial y} (x, y)_b'
            #   if n_subapertures < b <= 2 *n_apertures,
            # where b' = b - n_subapertures, and (x, y)_b denotes the relative
            # position of the center of the b-th subaperture assuming the entire
            # sensor grid is placed on the unit disk.
            d = np.full((n_zernike, 2 * n_ap), np.nan)#hier war np.nan
    
            # Compute evaluation position (x, y), that is, the relative positions
            # of the centers of the subapertures
            
            self.grid_size = round(np.sqrt(self.nFoci))
            
            
            """
            x_0 =  np.linspace((1 / self.grid_size - 1),
                                               (1 - 1 / self.grid_size),
                                               self.grid_size).reshape(1, -1)
            x_0 = np.repeat(x_0, self.grid_size, axis=0)
            y_0 =  np.linspace((1 - 1 / self.grid_size),
                                               (1 / self.grid_size - 1),
                                               self.grid_size).reshape(-1, 1)
            y_0 = np.repeat(y_0, self.grid_size, axis=1)
            midX = self.imageWidth/2
            midY = self.imageHeight/2
            lX = []
            lY = []
            
            for xi, conti in enumerate(x_0):
                for xj, conti in enumerate(x_0[xi]):
                    xAbs = x_0[xi,xj]*self.imageWidth/2+midX
                    yAbs = y_0[xi,xj]*self.imageHeight/2+midY
                    lX.append(xAbs)
                    lY.append(yAbs)
            
            #self.ax1.plot(lX, lY, 'o', color='black')
            
            """
            x_0 = []
            y_0 = []

            for cell in self.grid:
                if self.toRelImageCoords(cell.center)[0] == 0:
                    x_0.append(0.00000001)
                else:
                    x_0.append(self.toRelImageCoords(cell.center)[0])
                    
                if self.toRelImageCoords(cell.center)[1] == 0:
                    y_0.append(0.00000001)
                else:
                    y_0.append(self.toRelImageCoords(cell.center)[1])
           # print("meine")
            x_0 = np.array(x_0).reshape(self.grid_size,self.grid_size)
            y_0 = np.array(y_0).reshape(self.grid_size,self.grid_size)

                    
            #self.ax1.plot(lX, lY, 'o', color='black')
            
           # print(x_0.reshape(5,5))
           # print(y_0.reshape(5,5))
            # We compute the entries of D row by row, because rows correspond to
            # Zernike polynomials
            for row_idx, j in enumerate(range(1, n_zernike+1)):
    
                # Map single-index j to double-indices m, n
                m, n = zernike.j_to_mn(j)
    
                # Compute derivatives in x- and y-direction. For "small" values of
                # j, we can use the pre-computed derivatives from the fast_zernike
                # module. For even higher orders, the derivatives first need to be
                # computed "on demand", which is a lot slower.
                if j <= 135 and not j == 15 and not j ==21 and not j==28 and not j== 29 and not j ==36 and not j == 37:
                    x_derivatives: np.ndarray = \
                        fast_zernike.zernike_derivative_cartesian(m, n, x_0, y_0, 'x')
                    y_derivatives: np.ndarray = \
                        fast_zernike.zernike_derivative_cartesian(m, n, x_0, y_0, 'y')
                else:
                    zernike_polynomial = zernike.ZernikePolynomial(m=m, n=n).cartesian
                    x_derivatives = \
                       zernike.eval_cartesian(zernike.derive(zernike_polynomial, 'x'), x_0, y_0)
                    y_derivatives = \
                        zernike.eval_cartesian(zernike.derive(zernike_polynomial, 'y'), x_0, y_0)
    
                # Store derivatives in D matrix
                d[row_idx] = np.concatenate((x_derivatives.flatten(),
                                             y_derivatives.flatten()))
    
            # ---------------------------------------------------------------------
            # Find the Zernike coefficients by solving a linear equation system
            # ---------------------------------------------------------------------
    
            # Define the matrix E as per eq. (15) in [Cubalchini_1979]
            e = d @ d.transpose()
    
            # Finally, we can compute the coefficient vector of the wavefront.
            # According to eq. (16) in [Cubalchini_1979], we have:
            #   A = E^{-1} D P
            # Instead of computing the right-hand side directly by inverting E,
            # which is often ill-conditioned, resulting in major numerical
            # instabilities and incorrect fits, we transform this to:
            #   EA = DP,
            # and use a least squares solver to solve the  equation system for A.
            a = sp.linalg.lstsq(a=e, b=d @ p)[0]
    

            # Add an additional 0 in the first position for for Z^_0
            a = np.insert(a, 0, 0)
            print("calculated coeff Vector:")
            print(a)
            return a






















#Functions for the canvas for clearing etc.


    def draw(self):
        self.plotSensor.canvas.draw()
        self.plotSensor_2.canvas.draw()
        self.plotAnalyse.canvas.draw()
        self.plotSensor_3.canvas.draw()

    def plotClear(self):
        self.plotSensor.canvas.ax.cla()
        self.plotSensor.canvas.draw()
        self.plotSensor_3.canvas.ax.cla()
        self.plotSensor_3.canvas.draw()

        



    def saveRAW(self):
        
        app = QApplication(['./'])
        form = TXTSaveFileDialogWidget()
        if form.fname:
            np.savetxt(form.fname, self.image)
            size = len(form.fname)
            # Slice string to remove last 3 characters from string
            mod_string = form.fname[:size - 4]
            np.savetxt(mod_string+'_WaveFront.txt', self.calculatedWavGrid);

            
                       
            
    def save(self):
        
        app = QApplication(['./'])
        form = DummySaveFileDialogWidget()
        if form.fname:
            self.plotSensor.canvas.fig.savefig(form.fname,bbox_inches="tight");
            size = len(form.fname)
            # Slice string to remove last 3 characters from string
            mod_string = form.fname[:size - 4]
            self.plotSensor_2.canvas.fig.savefig(mod_string+'_WaveFront.pdf',bbox_inches="tight");

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    win = Window()
    win.show()
    sys.exit(app.exec())