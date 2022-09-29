# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:58:24 2022

@author: hi84qur
"""
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow,QHBoxLayout, QMessageBox, QMenu,QFormLayout,QLineEdit,QPushButton,QLabel
)

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtWidgets import (QApplication, QFileDialog, QWidget)
from PyQt5 import QtGui
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import zernike
import fast_zernike
import numpy as np
import matplotlib
import matplotlib as mpl
import matplotlib.colors as colors
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
class CoeffDialog(QWidget):
    
   def __init__(self, coeff, parent = None):
        """
        This Dialog is used to show a list of the calculated coefficients and their optical meaning
        it also enables the user to recalculate the wavefront using set coefficients
        
        Parameters
        ----------
        coeff : TYPE
            DESCRIPTION.
        parent : TYPE, optional
            DESCRIPTION. The default is None.
        
        Returns
        -------
        None.
        
        """
        super(CoeffDialog, self).__init__(parent)
        
        self.coeff = coeff
        self.opticalNames = ['Piston', 'Y-Tilt', 'X-Tilt', 'Oblique astigmatism', 'longitudinal Defocus', 'Vertical astigmatism', 'Vertical trefoil',
                        'Vertical coma', 'Horizontal coma', 'Oblique trefoil', 'Oblique quadrafoil', 'Oblique secondary astigmatism', 'Primary spherical',
                        'Vertical secondary astigmatism', 'Vertical quadrafoil']
        layout = QFormLayout()
        self.Lines = []
        percentages = []
        self.LinePercentages = []
        
        #calculate the percentages of the coresponding order
        
        summed = np.sum(np.absolute(coeff))
        
        
        for i, ko in enumerate(coeff):
            subLayout = QFormLayout()

            le = QLineEdit()
            if i < len(self.opticalNames):
                label = QLabel("j="+str(i)+' - '+self.opticalNames[i])
            else:
                label = QLabel("j="+str(i))
            le.setText(str(ko))
            self.Lines.append(le)  
            per = np.absolute(ko)/summed * 100
            lePercent = QLineEdit()
            percentages.append(per)
            lePercent.setText(str(per) + '%')
            
            self.LinePercentages.append(lePercent)
            subLayout.addRow(le,lePercent)
            layout.addRow(label,subLayout)
              
        self.btn = QPushButton("Recalculate Wavefront")
        self.btn.clicked.connect(self.reCalcWav)
        	
        layout.addRow(self.btn)
        self.setLayout(layout)
        self.setWindowTitle("Wavefront Editor")
        
        
        
		
   def reCalcWav(self):
      
      coefficients = []
      for line in self.Lines:
          coefficients.append(float(line.text()))
          
      
      summed = np.sum(np.absolute(coefficients))
      
      for i, ko in enumerate(coefficients):
          per = np.absolute(ko)/summed * 100
          self.LinePercentages[i].setText(str(per) + '%')
      
      self.mainWindowRef.calcCoeff = coefficients

      wavefront = zernike.Wavefront(coefficients=coefficients)     
      x_0, y_0 = zernike.get_unit_disk_meshgrid(resolution=1000)
      wf_grid = zernike.eval_cartesian(wavefront.cartesian, x_0=x_0, y_0=y_0)
  
      """

      """
      maximum = self.mainWindowRef.horizontalSlider.value() / 1000
      wf_grid[np.isnan(wf_grid)] = -1 
      self.mainWindowRef.calculatedWavGrid = wf_grid
      self.mainWindowRef.ax2.imshow(wf_grid, interpolation='nearest', cmap=self.mainWindowRef.colormap,
                      vmin=-maximum, vmax=maximum)
      
      self.mainWindowRef.ax2.set_xlim(0, len(self.mainWindowRef.calculatedWavGrid)-1)
      self.mainWindowRef.ax2.set_ylim(0,len(self.mainWindowRef.calculatedWavGrid))
      self.mainWindowRef.draw()
