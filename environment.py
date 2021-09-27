DEFAULT_WORLD_PARAMS = {
    'max_population'   : 200,
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

    
    def init_organisms(self):
        num_orgs = self.world_settings['max_population']

    def run_simulation(self, simulation_params):
        num_generations = simulation_params['generations']
        num_timesteps   = simulation_params['timesteps']

        for gen in range(num_generations):

            for t in range(num_timesteps):
                # run all creature interactions and fire their neural networks
                # this is done at each time step
                pass 

            # Now a whole generation is over and it is time to perform crossover
            # and mutation to set up the population for the next generation

            #===============COMPUTING FITNESS===================
            for organism in self.population:
                organism.compute_fitness()

            self.population.sort(reverse=True)    #sort will place lower elements first, so reverse=True will make them high to low


            #

