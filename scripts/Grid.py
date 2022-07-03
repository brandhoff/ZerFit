# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 16:32:36 2022

@author: Jonas
"""
import matplotlib.patches as patches
class Cell:
    def __init__(self, center, width, height = 0):
        """
        Is used as part of a grid, so the grid consists of 
        C x C cells each defined by a center and a with / height.
        The cell has its own coordsystem with the center being at 0,0:
        
        
    -1,1            1,1
        -----------
        |         |      
        |    c    |
        |         |
        -----------
    -1,-1             1,-1

        Parameters
        ----------
        center : Tupel(x,y)
            the center of the cell.
        width : float
            The dim of a cell.
        height : TYPE
            IF not provided  width = height.

        Returns
        -------
        None.

        """
        self.center = center
        self.x0 = center[0]
        self.y0 = center[1]
        self.width = width
        if height == 0:
            self.height = width
        else:
            self.height = height
            
            
            
    
    
    def drawRect(self, axis, color = 'red'):
        rect = patches.Rectangle((self.x0-self.width/2, self.y0-self.height/2), self.width, self.height, linewidth=1, edgecolor=color, facecolor='none')
        axis.add_patch(rect)
    
    def dotCenter(self, axis, color = 'pink'):
        """
        Draws a dot into the axis at the center of the cell

        Parameters
        ----------
        axis : mplAxis
            the axis to draw to.

        Returns
        -------
        None.

        """
        axis.plot(self.x0, self.y0, 'o', color=color)
        
    def abToRel(self, coords):
        """
        Transforms absolute coords to rel coords

        Parameters
        ----------
        coords : Tuepl(x,y)
            DESCRIPTION.

        Returns
        -------
        relative coords tupel.

        """
        if coords[0] > self.x0+self.width/2 or coords[1] > self.y0+self.height/2:
            print("NOT INSIDE CELL")
            return (0,0)
        if coords[0] < self.x0-self.width/2 or coords[1] < self.y0-self.height/2:
            print("NOT INSIDE CELL")
            return (0,0)
        xRel = (coords[0] - self.x0)/(self.width/2)
        yRel = (coords[1] - self.y0)/(self.height/2)

        return (xRel,yRel)
        
    
    def relToAb(self, coords):
        """
        Transforms relative coords to Absolute coords

        Parameters
        ----------
        coords : Tupel(x,y) of relative coords
            DESCRIPTION.

        Returns
        -------
        absolute coords tupel.

        """
        if coords[0] > 1 or coords[1] > 1:
            print("NOT INSIDE CELL")
            return (0,0)
        if coords[0] < -1 or coords[1] < -1:
            print("NOT INSIDE CELL")
            return (0,0)
        xAbs = coords[0] * self.width/2 + self.x0
        yAbs = coords[1] * self.height/2 + self.y0

        return (xAbs,yAbs)