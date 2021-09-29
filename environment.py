from numpy.lib.function_base import interp
from organism import Predator, Plant
from plotters import plot_organism, plot_plant

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

DEFAULT_WORLD_PARAMS = {
    'max_population'   : 60,
    'land_water_ratio' : 0.7,
    'day_length'       : 10000,   #number of simulation timesteps or ticks
    'day_night_ratio'  : 0.6,   #the ratio of day compared to night, from the total day_length
    'x_max'            : 2,
    'x_min'            : -2,
    'y_max'            : 2,
    'y_min'            : -2,
    'basic_distance'   : 0.05,    #defined as the amount of distance an organism need to travel to lose 1 point of energy. This is the minimum cost, but the organism's mass and other factors can make it costlier to move 
}

def fitness_function(**params):
    E_in  = params['energy_in']
    E_out = params['energy_out']
    traveled_dist = params['total_distance']

class World(object):
    '''Takes some parameters to create a world.
    A world can have different rates of organism spawn
    and food generation. It should also affect how 
    easily organisms can move through it, and the 
    availability of water and dangers'''

    def __init__(self, world_settings_dict):
        self.world_settings = world_settings_dict
        self.population = []    #this could be a class that makes sorting easier by overloading the comparison operators

    @property
    def basic_distance(self):
        return self.world_settings['basic_distance']

    def get_min_xy(self):
        return (self.world_settings['x_min'],self.world_settings['y_min'])

    def get_max_xy(self):
        return (self.world_settings['x_max'],self.world_settings['y_max'])

    def init_frame(self):
        fig, ax = plt.subplots()
        fig.set_size_inches(9.6, 5.4)

        x_min, y_min = self.get_min_xy()
        x_max, y_max = self.get_max_xy()

        plt.xlim([x_min + x_min * 0.25, x_max + x_max * 0.25])
        plt.ylim([y_min + y_min * 0.25, y_max + y_max * 0.25])

        # MISC PLOT SETTINGS
        ax.set_aspect('equal')
        frame = plt.gca()
        frame.axes.get_xaxis().set_ticks([])
        frame.axes.get_yaxis().set_ticks([])

        return fig, ax

    def render_frame(self, fig, ax, generation, timestep, *fig_params):
        #Here we do the plotting of the organisms and plants
        gen_count_text  = fig_params[0]
        t_count_text    = fig_params[1]
        total_orgs_text = fig_params[2]

        gen_count_text.set_text(f'GENERATION: {generation}')
        t_count_text.set_text(f'Timestep: {timestep}')
        total_orgs_text.set_text(f'Organisms Alive: {len(self.population)}')
        ax.clear()
        #fig.clear(True)

        x_min, y_min = self.get_min_xy()
        x_max, y_max = self.get_max_xy()

        plt.xlim([x_min + x_min * 0.25, x_max + x_max * 0.25])
        plt.ylim([y_min + y_min * 0.25, y_max + y_max * 0.25])
        
        for org in self.population:
            plot_organism(org,ax)

        # MISC PLOT SETTINGS
        ax.set_aspect('equal')
        frame = plt.gca()
        frame.axes.get_xaxis().set_ticks([])
        frame.axes.get_yaxis().set_ticks([])

        ax.plot()

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

    def run_simulation(self,simulation_params, ax=None):
        num_generations = simulation_params['generations']
        num_timesteps   = simulation_params['timesteps']

        self.init_organisms()
        #plt.ion()
        fig, ax = self.init_frame()
        gen_count_text  = fig.text(0.025, 0.95, "")
        t_count_text    = fig.text(0.025, 0.90, "")
        total_orgs_text = fig.text(0.025, 0.85, "")

        max_xy = self.get_max_xy()
        min_xy = self.get_min_xy()
        for gen in range(num_generations):
            for t in range(num_timesteps):
                self.render_frame(fig, ax, gen, t, gen_count_text, t_count_text, total_orgs_text)
                plt.pause(0.05)
                plt.draw()

                for org in self.population:
                    dist_traveled = org.move(max_xy,min_xy)

                    energy_penalty = dist_traveled / self.basic_distance
                    org.spend_energy(energy_penalty)
                    org.age += 1

                #================Remove dead organisms==================#
                self.population = [org for org in self.population if org.isalive()]
                if len(self.population) == 0:
                    break