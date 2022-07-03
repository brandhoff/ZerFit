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
import lmfit
from PyQt5.QtWidgets import (QApplication, QFileDialog, QWidget)
import zernike
import fast_zernike
from lmfit.lineshapes import gaussian2d, lorentzian
# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

class DummySaveFileDialogWidget(QWidget):

    def __init__(self, title="Save Graph", filters="Png File (*.png)"):
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
        self.grid = []
        self.nFoci = 25 #default
        self.relativeShifts = []
    def connectSignalsSlots(self):
        """
        This connects the button Presses etc with the corresponding action functions
        """
        self.btnTakeImage.clicked.connect(self.TestImageProcessing)
        self.btnShow.clicked.connect(self.reconstructWavefront)
        self.btnSavePDF.clicked.connect(self.save)

#Action Functions

    def TestImageProcessing(self):
        """
        This function is used for testing on an artificial image

        Returns
        -------
        None.

        """

        print("TEST Image")

        img = mpimg.imread('may.jpg')
        #img = mpimg.imread('singlePoint.jpg')
        image = np.zeros((1000, 1000))
        for i in range(len(img)):
            for j in range(len(img)):
                image[i,j] = np.sum(img[i,j])
        self.ax1.imshow(image, cmap = self.colormap)
        self.draw()
        
        self.guessList = []
        xy = peak_local_max(image, min_distance=7)#int((len(img))/self.nFoci-10))
        self.nFoci = 64#len(xy)

        
       #image_max = ndimage.maximum_filter(image, size=10, mode='constant')
        #self.ax2.imshow(image_max, cmap = self.colormap)


        for t in xy:
            self.ax1.plot(t[1], t[0], 'o', color='orange', alpha=0.5)
            self.guessList.append((t[1], t[0]))
            #self.fitLM2DGaussian(image, t[1], t[0], image[t[1],t[0]])
            #self.fit2DGaussian(image, t[1], t[0], image[t[1],t[0]])
        self.draw()
        self.buildAnalyticGrid(image, self.nFoci)
        self.drawGrid()
        self.ax1.set_xlim(0, len(image[0,:]))
        self.ax1.set_ylim(0, len(image[:,0]))
        self.draw()
        self.relativeShifts = []
        for foci in self.guessList:
            relShift = self.findCellForSpot(foci).addFocusCoords(foci)
            self.relativeShifts.append(relShift)
            
        coefficients = self.fit_wavefront(5)
        wavefront = zernike.Wavefront(coefficients=coefficients)     
        x_0, y_0 = zernike.get_unit_disk_meshgrid(resolution=1000)
        wf_grid = zernike.eval_cartesian(wavefront.cartesian, x_0=x_0, y_0=y_0)
        #wf_grid[np.isnan(wf_grid)] = -1 
        #self.ax2.imshow(wf_grid,cmap=self.colormap, vmin = 0,vmax = 0.2)
        limit = 1.1 * np.nanmax(np.abs(wf_grid))
        self.ax2.imshow(wf_grid, interpolation='nearest', cmap=self.colormap,
                        vmin=-limit, vmax=limit)
        
        self.ax2.set_xlim(0, len(image[0,:]))
        self.ax2.set_ylim(0, len(image[:,0]))
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


    def drawGrid(self):
        """
        Draws the Grid of Cells

        Returns
        -------
        None.

        """
        for cell in self.grid:
            cell.dotCenter(self.ax1, color = 'red')
            cell.drawRect(self.ax1)

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
        self.imageWidth = len(image[:,0])
        self.imageHeight = len(image[0,:])

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
            d = np.full((n_zernike, 2 * n_ap), np.nan)
    
            # Compute evaluation position (x, y), that is, the relative positions
            # of the centers of the subapertures
            
            self.grid_size = 8
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
                    x_0.append(0.000001)
                else:
                    x_0.append(self.toRelImageCoords(cell.center)[0])
                    
                if self.toRelImageCoords(cell.center)[1] == 0:
                    y_0.append(0.000001)
                else:
                    y_0.append(self.toRelImageCoords(cell.center)[1])
           # print("meine")
            x_0 = np.array(x_0)
            y_0 = np.array(y_0)
            """
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
                if j <= 135:
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
    def plotClear(self):
        self.plotSensor.canvas.ax.cla()
        self.plotSensor.canvas.draw()
        
        



    def save(self):
        
        app = QApplication(['./'])
        form = DummySaveFileDialogWidget()
        if form.fname:
            self.plotSensor.canvas.fig.savefig(form.fname,bbox_inches="tight");
            #plt.savefig(form.fname,bbox_inches="tight")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    win = Window()
    win.show()
    sys.exit(app.exec())