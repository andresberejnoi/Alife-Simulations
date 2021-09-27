from brain import Brain
from environment import World, DEFAULT_WORLD_PARAMS
from organism import Organism

import matplotlib.pyplot as plt

SIMULATION_PARAMS = {
    'generations': 1000,
    'timesteps'  : 100000,   #number of timesteps per generation
}

def main():
    world = World(DEFAULT_WORLD_PARAMS)
    world.init_organisms()

    world.run_simulation(SIMULATION_PARAMS)
