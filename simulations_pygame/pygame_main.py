'''
This script has been writen following the tutorial from:
https://www.youtube.com/watch?v=84njPYepKIU

on how to create a disease simulation using PyGame. 
I'm adapting it to my own artificial life simulations.
'''

import pygame
import numpy as np
import sys

from environment import Simulation
#from organism import Organism


if __name__ == '__main__':
    sim = Simulation()
    sim.start(20000)


