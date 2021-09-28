from organism import Predator, Plant
import matplotlib.pyplot as plt
from plotters import plot_organism, plot_plant
import numpy as np

DEFAULT_WORLD_PARAMS = {
    'max_population'   : 100,
    'land_water_ratio' : 0.7,
    'day_length'       : 10000,   #number of simulation timesteps or ticks
    'day_night_ratio'  : 0.6,   #the ratio of day compared to night, from the total day_length
    'map_width'        : 5000,
    'map_height'       : 5000,
}


class World(object):
    '''Takes some parameters to create a world.
    A world can have different rates of organism spawn
    and food generation. It should also affect how 
    easily organisms can move through it, and the 
    availability of water and dangers'''

    def __init__(self, world_settings_dict):
        self.world_settings = world_settings_dict
        self.population = []    #this could be a class that makes sorting easier by overloading the comparison operators

    def render_frame(self, generation, timestep):
        #code in this cell taken from here (some modifications): 
        #  https://github.com/nathanrooy/evolving-simple-organisms/blob/master/organism_v1.py
        fig, ax = plt.subplots()
        fig.set_size_inches(9.6, 5.4)

        x_min = -2
        x_max = 2

        y_min = -2
        y_max = 2

        plt.xlim([x_min + x_min * 0.25, x_max + x_max * 0.25])
        plt.ylim([y_min + y_min * 0.25, y_max + y_max * 0.25])

        #Here we do the plotting of the organisms and plants
        for org in self.population:
            plot_organism(org,ax)

        # MISC PLOT SETTINGS
        ax.set_aspect('equal')
        frame = plt.gca()
        frame.axes.get_xaxis().set_ticks([])
        frame.axes.get_yaxis().set_ticks([])


        plt.figtext(0.025, 0.95, f'GENERATION: {generation}')
        plt.figtext(0.025, 0.90, f'Timestep: {timestep}')

        fig.canvas.draw()
        fig.show()
        plt.pause(0.05)
        #plt.savefig(str(gen)+'-'+str(time)+'.png', dpi=100)
        #plt.pause(0.02)
        #plt.show()

    def init_organisms(self):
        num_orgs = self.world_settings['max_population']

        for i in range(num_orgs):
            rand_class = np.random.rand()
            if rand_class < 0.65:
                new_org = Predator()
            else:
                new_org = Plant()

            coord_tuple = np.random.uniform(-2,2,2)
            angle = np.random.randint(0,361) 
            new_org.set_position_dir(coord_tuple, angle)
            self.population.append(new_org)

    def run_simulation(self, simulation_params, ax=None):
        num_generations = simulation_params['generations']
        num_timesteps   = simulation_params['timesteps']

        self.init_organisms()

        for gen in range(num_generations):

            for t in range(num_timesteps):
                # run all creature interactions and fire their neural networks
                # this is done at each time step
                self.render_frame(gen,t)
                #plt.pause(0.02)
                #plt.show()
                
                
                for org in self.population:
                    org.move()

            # Now a whole generation is over and it is time to perform crossover
            # and mutation to set up the population for the next generation

            #===============COMPUTING FITNESS===================
            for organism in self.population:
                organism.compute_fitness()

            self.population.sort(reverse=True)    #sort will place lower elements first, so reverse=True will make them high to low


            #

