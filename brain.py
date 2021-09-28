import numpy as np

class Brain(object):
    def __init__(self, params_dict=None):
        if params_dict is None:
            pass 

        
    def make_decision(self, inputs=None):
        #inputs will be an array of different sensor data for the organism
        #outputs will be the amount of distance to travel (0 to 1), and the direction (as an angle)
        val = np.random.rand(2)    #will create an array of 2 elements, each with a random value [0-1]
        val[1] *= 360    #this will make the angle be a value between [0-360]

        return val