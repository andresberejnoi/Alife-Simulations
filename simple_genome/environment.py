from tools import make_random_genome
import numpy as np

class World(object):
    BARRIER = 100
    WATER   = 20
    WORLD_EGDE = -1    #this could be the same as barrier, but I will keep a separate variable for it

    def __init__(self, width=1000, height=1000, padding_thickness = 10):
        self.width             = width
        self.height            = height
        self.padding_thickness = padding_thickness
        self.init_world()

    def init_world(self):
        '''This function needs some tweaking to deal with higher than 2D worlds'''
        _grid = np.zeros(shape=(self.width, self.height), dtype=np.int8)   #create 2D matrix to store the map
        self.grid = np.pad(_grid, self.padding_thickness, constant_values=self.WORLD_EGDE)

        num_pheromone_channels = 3
        _pheromone_grid = np.zeros(shape=(self.width, self.height, num_pheromone_channels))
        self.pheromone_grid = np.pad(_pheromone_grid, self.padding_thickness, constant_values=self.WORLD_EGDE)

    def get_surroundings(self, x, y, radius=1):
        '''Return a sub-grid of the surronding squares to center_xy. The size of the sub-grid depends
        on the radius. A radius of 1 means that we get back a 3x3 square:
                                1,  1, 1
                                1, xy, 1
                                1,  1, 1
        '''
        assert(radius>=1)
        #assert(radius<=self.padding_thickness)   #this assert should be changed. It is not as simple as this
  
        cx, cy = x, y

        #Apply padding offset
        cx += self.padding_thickness
        cy += self.padding_thickness

        dx = dy = radius
        return self.grid[cy-dy:cy+dy+1, cx-dx:cx+dx+1]   #the +1 adjusts to get the upper bound included

    def __repr__(self):
        return f"<World: h={self.height}, w={self.width}>"
  
    @property
    def size(self):
        return (self.height, self.width)

    

class Simulation(object):
    def __init__(self, width=500, height=500, max_population=200, factory=None, steps_per_generation=300):
        self.world_width    = width
        self.world_height   = height
        self.max_population = max_population

        self.factory        = factory
        self.population     = []
        self.world          = World(width, height)   #initialize empty world

    def start(self):
        self.current_gen = 0   #generation number
        self.t_step      = 0   #timestep for current generation

    def populate_world(self, init_population=20):
        assert(init_population <= self.max_population)

        for i in range(init_population):
            genome = make_random_genome(num_genes=30, num_brain_connections=25)

            min_x, min_y = 0, 0
            max_x, max_y = self.world_width, self.world_height
            x = np.random.randint(min_x, max_x)
            y = np.random.randint(min_y, max_y)

            org = self.factory.create_organism(genome)   #create new organism
            org.set_pos(x,y)
            org.set_pos_boundaries(min_xy=(min_x,min_y), max_xy=(max_x,max_y))
            self.population.append(org)



    def advance_simulation(self):
        '''Computes all the changes for the next cycle'''
        for i, org in enumerate(self.population):
            #TODO: first compute collisions with every other organism and the environment (create a list of changes to params)
            collisions = self.compute_collisions()

            #TODO: 
            actions = org.think()   #make organism think
            #compute_next_params()
            #check for collisions and prepare new positions (inspired by (line 79): https://github.com/rafael-fuente/Ideal-Gas-Simulation-To-Verify-Maxwell-Boltzmann-distribution/blob/6e87568cb6103a391c6098d447142a74611674c4/Ideal%20Gas%20simulation%20code.py#L79)
            

    