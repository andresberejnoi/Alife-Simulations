from tools import make_random_genome
import numpy as np

class World(object):
    def __init__(self, width=1000, height=1000):
        self.width = width
        self.height = height
        self.init_world()

    def init_world(self):
        self.grid = np.zeros(shape=(self.width, self.height))   #create 2D matrix to store the map


class Simulation(object):
    def __init__(self, width=500, height=500, max_population=200, factory=None):
        self.world_width    = width
        self.world_height   = height
        self.max_population = max_population

        self.factory        = factory
        self.population     = []
        self.world          = World(width, height)

    def start(self):
        self.current_gen = 0   #generation number
        self.t_step      = 0   #timestep for current generation

    def populate_world(self, init_population=20):
        assert(self.max_population == init_population)

        for i in range(init_population):
            genome = make_random_genome(num_genes=30, num_brain_connections=25)
            self.population.append(self.factory.create_organism())

    def simulation_step(self):
        for org in self.population:
            actions = org.think()