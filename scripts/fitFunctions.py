# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 14:34:29 2022

@author: Jonas Brandhoff
for Friedrich Schiller Universität
"""
import numpy as np
def twoD_Gaussian(xdata_tuple, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
        """
        A 2D Gaussian Function for fitting a spot

        Parameters
        ----------
        xdata_tuple : TYPE
            The data of the 2D plane.
        amplitude : TYPE
            init guess of the amplitude.
        xo : TYPE
            init guess of the x0 pos.
        yo : TYPE
            init guess of the y0 pos.
        sigma_x : TYPE
            sigma in x direction in case of a circle restraint to sigma_y.
        sigma_y : TYPE
            sigma in y direction in case of a circle restraint to sigma_x.
.
        theta : TYPE
            theta parameter.
        offset : TYPE
            offset from zer.

        Returns
        -------
        TYPE
            the constructed model of trhe 2D gaussian.

        """
        x,y = xdata_tuple
        xo = float(xo)
        yo = float(yo)    
        a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
        b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
        c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
        g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) 
                                + c*((y-yo)**2)))
        return g.ravel()