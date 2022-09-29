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
from lmfit.models import Gaussian2dModel,ConstantModel
from lmfit import Model, Parameters
import Grid
import CameraCalibration
import lmfit
from PyQt5.QtWidgets import (QApplication, QFileDialog, QWidget)
from PyQt5 import QtGui
from PyQt5.QtCore import QEvent
import zernike
import fast_zernike
import CoeffDialog
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
    #Ein autokorrekteur fuer tip und tilt
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
        self.progressBar.setMinimum(0)
        
        

    def connectSignalsSlots(self):
        """
        This connects the button Presses etc with the corresponding action functions
        """
        self.btnTakeImage.clicked.connect(self.TestImageProcessing)
        self.btnShow.clicked.connect(self.reconstructWavefront)
        self.btnSavePDF.clicked.connect(self.save)
        
        
        self.btnSave_3.clicked.connect(self.clickedWavInfo)
        
        
        #slider
        self.horizontalSlider.valueChanged.connect(self.updateWav)
        self.sliderAnalyse.valueChanged.connect(self.updateAnalyseView)

        
        self.btnCreateGrid.clicked.connect(self.clickShowGrid)
        
        
        #self.btnFindSpots.clicked.connect(self.findSpotInGrid_singleCell)
        
        self.btnFindSpots.clicked.connect(self.clickedSpotsFinder)
        
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
        
        self.btnCaliGridFix.clicked.connect(self.fixGrid)
        
        self.btnCaliSaveGrid.clicked.connect(self.saveCreatedGridToFile)
        self.btnCaliLoadGrid.clicked.connect(self.openCreatedGridFromFile)
        
        #Navigation buttons for ROI
        self.btnCaliUp.clicked.connect(self.clickROIup)
        self.btnCaliDown.clicked.connect(self.clickROIdown)
        self.btnCaliLeft.clicked.connect(self.clickROIleft)
        self.btnCaliRight.clicked.connect(self.clickROIright)
        self.sliderCaliRadius.valueChanged.connect(self.RadiusChanged)


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
        
        self.ax2.set_xlim(0, len(self.calculatedWavGrid)-1)
        self.ax2.set_ylim(0,len(self.calculatedWavGrid))
        self.draw()

    def updateWav(self):
        if self.calculatedWavGrid is None:
            return
        else:
            self.ax2.cla()
            maximum = self.horizontalSlider.value() / 1000
        
            self.ax2.imshow(self.calculatedWavGrid, interpolation='nearest', cmap=self.colormap,
                        vmin=-maximum, vmax=maximum)
            self.ax2.set_xlim(0, len(self.calculatedWavGrid)-1)
            self.ax2.set_ylim(0, len(self.calculatedWavGrid))
            self.plotSensor_2.canvas.draw()




    def clickedWavInfo(self):
        coeff = self.calcCoeff
        self.Coeffdialog = CoeffDialog.CoeffDialog(coeff)
        self.Coeffdialog.mainWindowRef = self
        #self.Coeffdialog.canvas = self.plotSensor_2.canvas
        self.Coeffdialog.show()


    def clickShowGrid(self):
        """
        This will draw the given grid for the window of the fitting process ax1
        

        Returns
        -------
        None.

        """
        self.drawGrid(axis = self.ax1)
        self.draw()

    def buildGrid(self, axis = None):
        """
        this function will build a grid for the taken and cut img
        you can provide an axis in which the grid should be drawn default is the
        axis of the fitting window ax1

        Returns
        -------
        None.

        """
        self.buildAnalyticGrid(self.image, self.nFoci)
        self.drawGrid(axis = axis)
        self.draw()


    def clickedSpotsFinder(self):
        if self.checkBoxAutomatic.isChecked():
            self.findSpotInGridUsingGaussian()
        else:
            self.findSpotInGrid()


    def findSpotInGrid(self):
        """
        Finds all spots, does not look inside a cell but associates a cell with a found spot

        Returns
        -------
        None.

        """
        self.relativeShifts = []
        #Die foci guesses als init guess der gaussfunktionen nehmen:
        globalGuess = self.fociGuess.tolist()
        flagNoSpot = False
        for cell in self.grid:
            img = self.image
            lowerleft = cell.relToAb((-1,-1)) #unten links
            upperright = cell.relToAb((1,1))#oben rechts
            x0 = 0
            y0 = 0
            foundSpot = False
            for item in globalGuess:
                if cell.isInside((item[1],item[0])):
                    x0 = item[1]
                    y0 = item[0]
                    self.ax1.plot(x0, y0, 'x', color='green')
                    cell.hasSpot = True
                    cell.spot = item
                    globalGuess.remove(item)
                    foundSpot = True
                    break
            if not foundSpot:
                flagNoSpot = True
            (relItemX, relItemY) = cell.abToRel((x0,y0))
            self.relativeShifts.append((relItemX, relItemY))
        if len(globalGuess) > 0:
            for item in globalGuess:
                self.ax1.plot(item[1], item[0], 'x', color='red')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Too many Spots Found")
            msg.setInformativeText('While trying to find a Spot inside a cell multiple were found! Maybe the wavefront is too curved. If this was intended the code will proceed as if the first guess was the best!')
            msg.setWindowTitle("Error")
            msg.exec_()
        if flagNoSpot:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Cells without Spot!")
            msg.setInformativeText('While trying to find a Spot inside a cell no Spot was found. This code will behave as if there is no shift present for this cell!')
            msg.setWindowTitle("Error")
            msg.exec_()
        self.draw()
        if self.checkBoxCorrectTipTilt.isChecked():
            print("now Im correcting tip and tilt")
            flagCorrectX = True
            flagCorrectY = True
            meanX = np.mean((self.relativeShifts[:])[0])
            meanY = np.mean((self.relativeShifts[:])[1])
            for relShift in self.relativeShifts:
                if relShift[0] * meanX < 0:
                    flagCorrectX = False
                if relShift[1] * meanY < 0:
                    flagCorrectY = False
                    
            #self.relativeShifts = self.relativeShifts - (meanX, meanY)
            if flagCorrectX or flagCorrectY:
                for i, relShift in enumerate(self.relativeShifts):
                    if flagCorrectX:
                       self.relativeShifts[i] = ((self.relativeShifts[i])[0] -meanX,(self.relativeShifts[i])[1])
                    if flagCorrectY:
                       self.relativeShifts[i] = ((self.relativeShifts[i])[0],(self.relativeShifts[i])[1] -meanY)








    def findSpotInGridUsingGaussian(self):
        """
        Trys to Fit a 2D Gaussian for each build cell

        Returns
        -------
        None.

        """
        self.relativeShifts = []
        lastSigma = 0
        lastAmpl = 0
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(len(self.grid))
        
        for index, cell in enumerate(self.grid):
            self.progressBar.setValue(index)
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
                if cell.isInside((item[1],item[0])):
                    x0 = item[1]
                    y0 = item[0]
                    cell.hasSpot = True
                    cell.spot = item
                    break
            #x0-lowerleft[1]
            #y0-lowerleft[0]
            result, mesh = self.fitLM2DGaussian(sliecedCell, x0 = x0, y0 = y0, ampl = lastAmpl, sigma = lastSigma, lowerleft = lowerleft)
            
            x = mesh[0]#+lowerleft[1]
            y = mesh[1]#+lowerleft[0]
            #report = lmfit.fit_report(result.params)
            px = result.params['peak_centerx'].value
            py = result.params['peak_centery'].value
            #print(lowerleft)
            
            #print(x)
            #print(y)
            #px = px
            #py = py

            lastSigma = result.params['peak_sigmax'].value
            lastAmpl = result.params['peak_amplitude'].value

            (relItemX, relItemY) = cell.abToRel((px,py))
            self.relativeShifts.append((relItemX, relItemY))
            self.ax1.contour(x, y, result.best_fit,  colors='black')
            #self.ax1.contour(x, y, result.best_fit,[0.5,1,1.5,2],  colors='black')

            self.draw()
        self.progressBar.setValue(0)





    def findSpotInGrid_singleCell(self):
        """
        Finds all spots for all cells, looks only for spots inside of each cell
        This function is currently unused due to its inaccurate nature.
        
        The min max search for the whole ROI is somewhat equally fast but more percise.
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
#--------------------------CAMERA Calibration-------------------------
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
        if self.Camera.connectCamera(textWidget = self.textCaliCamera):
            self.connected = True

    def clickDisconnect(self):
        if self.connected:
            self.Camera.disconnectCamera()
            self.textCaliCamera.setText('')

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
        
        #yx = peak_local_max(img, min_distance = 20, exclude_border = 0)
        yx = peak_local_max(img, min_distance = 20, exclude_border = 0, threshold_rel = float(self.spinRelInt.value()))

        print("I guessed a grid of size:")
        print(round(np.sqrt(len(yx))))
        self.gridGuess = round(np.sqrt(len(yx)))**2
        self.fociGuess = yx
        image = img
        self.nFoci = self.gridGuess
        print(self.nFoci)
        self.image = image
        self.imageHeight = len(image[0,:])
        self.imageWidth = len(image[:,0])
        
        self.axCali.plot(yx[:,1], yx[:,0], 'x', color='green')

        self.buildGrid(axis = self.axCali)
        self.axCali.set_xlim(0, self.imageWidth-1)
        self.axCali.set_ylim(0,self.imageHeight-1)

    def fixGrid(self):
        """
        This fixes a given grid for the number of spots identified. this is accieved using the mean distance
        between each spot in a givn cell.
        for this all the spots are computed and associated with a cell.
        Afterwards the image will be streched in a way that each spot lies in the center of a grid cell.
        Please note that for this the correct amount of spots in the image is needed!

        Returns
        -------
        None.

        """
        
        
        """
        if self.checkCaliCircular.isChecked():



            unsorted_fociList = self.fociGuess
            fociList = []
            globalGuess = unsorted_fociList.tolist()
            for cell in self.grid:
                for item in globalGuess:
                    if cell.isInside((item[1],item[0])):
                        fociList.append(item)
                        globalGuess.remove(item)
                        cell.hasSpot = True
                        cell.spot = item
            tempGrid = []            
            for i, cell in enumerate(self.grid):
                if cell.hasSpot:
                    tempGrid.append(cell)
            self.grid = tempGrid

            print('lengh')
            print(len(self.grid))
            self.axCali.cla()
            self.drawGrid(axis = self.axCali)
            self.axCali.imshow(self.cutImg, cmap = self.colormap)
            self.axCali.set_xlim(0, self.imageWidth-1)
            self.axCali.set_ylim(0,self.imageHeight-1)
            self.draw()
                
                
                
                
                
                
                
        else:
        """
        cellZahl = self.nFoci
        unsorted_fociList = self.fociGuess
        fociList = []
        #sort the foci from lower left upwards and then right
        globalGuess = unsorted_fociList.tolist()
        missingSpot = False
        for cell in self.grid:
            flagHasSpot = False
            for item in globalGuess:
                if cell.isInside((item[1],item[0])):
                    fociList.append(item)
                    globalGuess.remove(item)
                    flagHasSpot = True
                    cell.hasSpot = True
                    cell.spot = item
                    break
            if not flagHasSpot:
                missingSpot = True
        #if there are cells without spots we have a small problem
        #we then have to use a different method to compute d
        #So instead we cycle thru all the cells and check if both have a spot
        if missingSpot:
            print("oh no a cell does not have a spot yikes")
            ds = []
            UpperBound = len(self.grid) - round(np.sqrt(len(self.grid)))
            for i in range(UpperBound):
                ShiftRight = i + round(np.sqrt(len(self.grid)))
                if self.grid[i].hasSpot and self.grid[ShiftRight].hasSpot:
                    ds.append(self.grid[ShiftRight].spot[1] - self.grid[i].spot[1])
            d = round(np.mean(ds))
            print('calculated d')
            print(str(d))
            x0 = self.grid[0].x0-d/2 + self.Camera.center[0] - self.Camera.radius 
            y0 = self.grid[0].y0-d/2 + self.Camera.center[1] - self.Camera.radius
            self.buildKnownGrid(len(self.grid), d, (x0,y0))
            self.axCali.cla()
            centerShift = (round(np.sqrt(len(self.grid)))*d)/2
            self.Camera.center = (round(x0 + round(centerShift)), round(y0+round(centerShift)))
            self.Camera.radius = round((np.sqrt(len(self.grid))*d)/2)    
        else:    
            #Calculate distance d
            UpperBound = cellZahl - round(np.sqrt(cellZahl))
            ds = []
            for i in range(UpperBound):
                di = ((fociList[i+round(np.sqrt(cellZahl))])[1]-(fociList[i])[1])
                ds.append(di)
                
            d= round(np.mean(ds))
            #print("bestimmte distance: ")
            #print(str(d))
            #Build Grid from known d and n
            x0 = (fociList[0])[1]-d/2 + self.Camera.center[0] - self.Camera.radius 
            y0 = (fociList[0])[0]-d/2 + self.Camera.center[1] - self.Camera.radius
            self.buildKnownGrid(cellZahl, d, (x0,y0))
            #fix the camera view so that the grid is inside the image:
            self.axCali.cla()
            centerShift = (round(np.sqrt(cellZahl))*d)/2
            #print('center x')
            #print(str(round(x0 + round(centerShift))))
            #print('center y')
            #print(str(round(y0+round(centerShift))))
            #print('Radius')
            #print(str(round((np.sqrt(cellZahl)*d)/2)))
            self.Camera.center = (round(x0 + round(centerShift)), round(y0+round(centerShift)))
            self.Camera.radius = round((np.sqrt(cellZahl)*d)/2)    
        cutImg = self.Camera.cutImageToAreaOfInterest(self.deepCopyImg)
        self.axCali.imshow(cutImg, cmap = self.colormap)
        self.cutImg = cutImg
        self.tellMeAboutFoci(cutImg)
        self.draw()


#---------------------------------------------------------------------
#---------------------------------------------------------------------
#--------------------------Navigation Buttons-------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------

    def clickROIup(self):
        self.axCali.cla()
        
        (centerX, centerY) = self.Camera.center
        self.Camera.center = (centerX, centerY-1)
        
        cutImg = self.Camera.cutImageToAreaOfInterest(self.deepCopyImg)
        self.axCali.imshow(cutImg, cmap = self.colormap)
        self.cutImg = cutImg
        if self.checkCaliTrack.isChecked():
                self.tellMeAboutFoci(cutImg)
        self.draw()

    def clickROIdown(self):
        self.axCali.cla()
        
        (centerX, centerY) = self.Camera.center
        self.Camera.center = (centerX, centerY+1)
        
        cutImg = self.Camera.cutImageToAreaOfInterest(self.deepCopyImg)
        self.axCali.imshow(cutImg, cmap = self.colormap)
        self.cutImg = cutImg
        if self.checkCaliTrack.isChecked():
                self.tellMeAboutFoci(cutImg)
        self.draw()   
        
        
    def clickROIleft(self):
        self.axCali.cla()
        
        (centerX, centerY) = self.Camera.center
        self.Camera.center = (centerX+1, centerY)
        
        cutImg = self.Camera.cutImageToAreaOfInterest(self.deepCopyImg)
        self.axCali.imshow(cutImg, cmap = self.colormap)
        self.cutImg = cutImg
        if self.checkCaliTrack.isChecked():
                self.tellMeAboutFoci(cutImg)
        self.draw()


    def clickROIright(self):
        self.axCali.cla()
        
        (centerX, centerY) = self.Camera.center
        self.Camera.center = (centerX-1, centerY)
        
        cutImg = self.Camera.cutImageToAreaOfInterest(self.deepCopyImg)
        self.axCali.imshow(cutImg, cmap = self.colormap)
        self.cutImg = cutImg
        if self.checkCaliTrack.isChecked():
                self.tellMeAboutFoci(cutImg)
        self.draw()

    def RadiusChanged(self):
        if int(self.axCali.get_ylim()[1]) == len(self.cutImg[0,:])-1:
            self.axCali.cla()
            radius = self.sliderCaliRadius.value()
            self.Camera.radius = radius
            cutImg = self.Camera.cutImageToAreaOfInterest(self.deepCopyImg)
            self.axCali.imshow(cutImg, cmap = self.colormap)
            self.cutImg = cutImg
            if self.checkCaliTrack.isChecked():
                self.tellMeAboutFoci(cutImg)
            self.draw()


    def saveCreatedGridToFile(self):
        ROIcenter = self.Camera.center
        ROIradius = self.Camera.radius
        nFoci = self.nFoci
        
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Grid', 
         'c:\\',"Grid file (*.grid)")
        if filename:
            f = open(filename, "w")
            f.write(str(ROIcenter[0])+'\n')
            f.write(str(ROIcenter[1])+'\n')
            f.write(str(ROIradius)+'\n')
            f.write(str(nFoci))
            f.close()
            
    def openCreatedGridFromFile(self):
        ROIcenterX = 0
        ROICenterY = 0
        ROIradius = 0
        nFoci = 0        
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Grid', 
         'c:\\',"Grid file (*.grid)")
        if filename:
            f = open(filename, 'r')
            Lines = f.readlines()
            ROIcenterX = int(Lines[0])
            ROIcenterY = int(Lines[1])
            ROIradius = int(Lines[2])
            nFoci = int(Lines[3])
            f.close()
        if nFoci > 0:
            self.axCali.cla()
            self.draw()
            self.Camera.center = (ROIcenterX,ROIcenterY)
            self.Camera.radius = ROIradius
            self.nFoci = nFoci
            self.gridGuess = nFoci
            cutImg = self.Camera.cutImageToAreaOfInterest(self.deepCopyImg)
            self.axCali.imshow(cutImg, cmap = self.colormap)
            self.cutImg = cutImg
            self.buildGrid(axis = self.axCali)
            
            self.image = cutImg
            self.imageHeight = len(cutImg[0,:])
            self.imageWidth = len(cutImg[:,0])
            
            self.axCali.set_xlim(0, self.imageWidth-1)
            self.axCali.set_ylim(0,self.imageHeight-1)
            
            
            yx = peak_local_max(cutImg, min_distance = 20, exclude_border = 0, threshold_rel = 0.2)
            self.fociGuess = yx
            
            self.draw()
            
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

    def fitLM2DGaussian(self, image, x0 = 0, y0=0, ampl=0, sigma = 0, lowerleft = (0,0)):
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
         
        img = image
        #img[img < 0.1*np.max(image)] = 0
        #img = np.matrix.round(img)
        
        x1 = np.linspace(lowerleft[0], lowerleft[0]+len(image[:,0]), len(image[:,0]))
        y1 = np.linspace(lowerleft[1], lowerleft[1]+len(image[0,:]), len(image[0,:]))
        x, y = np.meshgrid(x1, y1)
        
        
        
        maxz = np.amax(img)
        minz = np.amin(img)
        maxx = lowerleft[0]+len(image[:,0])
        minx = lowerleft[0]
        
        maxy = lowerleft[1]+len(image[0,:])
        miny = lowerleft[1]
        
        
        height = (maxz - minz)
        sigmax = (maxx-minx)/6.0
        sigmay = (maxy-miny)/6.0
        amp = height*sigmax*sigmay
        
        #amp = ampl
        #if ampl > 0:
            
        if sigma > 0:
            sigmax = sigma
        fit_model = Gaussian2dModel(prefix='peak_')
        params = Parameters()
       
      
        
        params.add_many(
            ('peak_'+'amplitude', amp, True, 0, amp*1.5),
            ('peak_'+'centerx', x0, True, x0-0.005*x0, x0+0.005*x0),
            ('peak_'+'centery', y0, True, y0-0.005*y0, y0+0.005*y0),
            ('peak_'+'sigmax', sigmax, True, 0, sigmax*1.5))
        params.add('peak_sigmay', expr='peak_sigmax')
        if sigma > 0: 
            params.add('peak_sigmax', sigma, True, min = sigma - 0.05*sigma, max = sigma+ 0.05*sigma)
        #if ampl >0:
           # params.add('peak_amplitude', ampl, True, ampl- 0.05*ampl,  ampl+ 0.05*ampl)


        result = fit_model.fit(img, params, x=x, y=y)
        mesh = (x,y)
        return result, mesh




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
            
            
    def buildKnownGrid(self, nFoci, width, pos0):
        """
        

        Parameters
        ----------
        nFoci : Number of foci
            DESCRIPTION.
        width : width of a cell
            DESCRIPTION.
        pos0 : lowe left corner
            DESCRIPTION.

        Returns
        -------
        None.

        """
        x0 = pos0[0]
        y0 = pos0[1]
        cellWidth = width
        cellHeight = cellWidth
        self.grid = []
        numPer = round(np.sqrt(nFoci))
        for xi in range(numPer):
            for yi in range(numPer):
                posX = cellWidth/2 + xi * cellWidth
                posY = cellHeight/2 + yi * cellHeight
                cell = Grid.Cell((posX,posY),cellWidth, height = cellHeight)
                self.grid.append(cell)
        
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