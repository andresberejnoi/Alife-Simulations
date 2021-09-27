from brain import Brain
from environment import World, DEFAULT_WORLD_PARAMS
from organism import Organism

import matplotlib.pyplot as plt

SIMULATION_PARAMS = {
    'generations'   : 1000,
    'timesteps'     : 100000,   #number of timesteps per generation
    'mutation_rate' : 0.03,     #not sure if this should go into world parameters or here, or if there should be only one global parameter variable
}

def main():
    world = World(DEFAULT_WORLD_PARAMS)
    world.init_organisms()

    world.run_simulation(SIMULATION_PARAMS)
