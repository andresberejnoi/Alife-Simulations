'''
Includes some convenience plotting functions for 
different organisms. Most of the code here was taken
from this repository's file:
https://github.com/nathanrooy/evolving-simple-organisms/blob/master/plotting.py
'''

from matplotlib import pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
import matplotlib.lines as lines

from math import sin
from math import cos
from math import radians

#--- FUNCTIONS ----------------------------------------------------------------+

def plot_organism(organism, ax):

    x1          = organism.x_pos
    y1          = organism.y_pos
    orientation = organism.direction

    rgba         = organism.get_rgba()  #this is a tuple of (R,G,B,Alpha)
    num_vertices = organism.genes['num_sides']
    radius       = organism.genes['radius']      
    
    
    #circle = Circle([x1,y1], 0.05, edgecolor = 'g', facecolor = rgba, zorder=8)
    #ax.add_artist(circle)

    shape = RegularPolygon([x1,y1], num_vertices, radius, orientation, facecolor=rgba, zorder=8)
    ax.add_artist(shape)

    edge  = RegularPolygon([x1,y1], num_vertices, radius, orientation, facecolor='None', edgecolor='darkblue', zorder=8)
    ax.add_artist(edge)
    #edge = Circle([x1,y1], 0.05, facecolor='None', edgecolor = 'darkgreen', zorder=8)
    #ax.add_artist(edge)

    tail_len = 0.075
    
    x2 = cos(radians(orientation)) * tail_len + x1
    y2 = sin(radians(orientation)) * tail_len + y1

    ax.add_line(lines.Line2D([x1,x2],[y1,y2], color='darkgreen', linewidth=1, zorder=10))

    pass


def plot_plant(organism, ax):
    x1    = organism.x_pos
    y1    = organism.y_pos

    rgba = organism.get_rgba()
    circle = Circle([x1,y1], 0.03, edgecolor = 'darkslateblue', facecolor = 'mediumslateblue', zorder=5)
    ax.add_artist(circle)
    
    pass