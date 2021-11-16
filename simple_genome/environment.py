from action_outputs import perform_actions
from tools import make_random_genome, show_org_info
import numpy as np

#---Set up RGB Colors
GREEN  = (0  , 255,   0)
RED    = (255,   0,   0)
BLUE   = (0  ,   0, 255)
YELLOW = (255, 255,  50)
BLACK  = (0  ,   0,   0)
WHITE  = (255, 255, 255)
PURPLE = (150,  50, 255)
BROWN  = (150, 130, 130)

class World(object):
    BARRIER    = 100
    WATER      = 20
    WORLD_EGDE = 255    #this could be the same as barrier, but I will keep a separate variable for it
    EMPTY      = 0
    PLANT      = 1
    HERBIVORE  = 2
    CARNIVORE  = 3
    OMNIVORE   = 4

    OBJECT_TYPES = {
        'water'      : WATER,
        'world_edge' : WORLD_EGDE,
        'barrier'    : BARRIER,
        'empty'      : EMPTY,
        'plant'      : PLANT,
        'herbivore'  : HERBIVORE,
        'carnivore'  : CARNIVORE,
        'omnivore'   : OMNIVORE,
    }

    color_dict = {
        WORLD_EGDE : BLACK,
        BARRIER    : BROWN,
        EMPTY      : WHITE,
        PLANT      : GREEN,
        HERBIVORE  : YELLOW,
        CARNIVORE  : RED,
        OMNIVORE   : PURPLE,
        WATER      : BLUE

    }

    def __init__(self, width=1000, height=1000, padding_thickness = 10):
        self.width             = width
        self.height            = height
        self.padding_thickness = padding_thickness
        self.init_world()

    def init_world(self):
        '''This function needs some tweaking to deal with higher than 2D worlds'''
        #_grid = np.zeros(shape=(self.height, self.width), dtype=np.int8)   #create 2D matrix to store the map
        #_grid.fill()
        _grid = np.full((self.height, self.width), self.EMPTY, dtype=np.uint8)
        self.grid = np.pad(_grid, self.padding_thickness, constant_values=self.WORLD_EGDE)

        num_pheromone_channels = 3
        _pheromone_grid = np.zeros(shape=(self.height, self.width, num_pheromone_channels))
        self.pheromone_grid = np.pad(_pheromone_grid, self.padding_thickness, constant_values=self.WORLD_EGDE)
    
    def clear_grids(self):
        pad = self.padding_thickness
        self.grid[pad:-pad, pad:-pad] = self.EMPTY

        #TODO: also clear the pheromone grid and any other grids 

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

    def get_empty_spot(self):
        '''return row,colum of a random coordinate of the world which is empty. 
        This method will be called several times as it is now. It would be more efficient to
        do a single call and select a bunch of empty spots from the beginning. 
        '''
        #TODO: make this function efficient and reduce call numbers
        rng = np.random.default_rng()
        empty_slots = np.where(self.grid == self.EMPTY)
        empty_slots = list(zip(*empty_slots))   #create a list of coordinates : [(row,col), (row,col), ..., etc]

        idx = rng.integers(0, len(empty_slots))
        row, col = empty_slots[idx]
        return row, col

    def get_random_empty_spots(self, num_spots):
        rng = np.random.default_rng()
        empty_slots = np.where(self.grid == self.EMPTY)
        empty_slots = list(zip(*empty_slots))   #create a list of coordinates : [(row,col), (row,col), ..., etc]

        selected_spots = []
        for i in range(num_spots):
            idx  = rng.integers(0, len(empty_slots))
            slot = empty_slots.pop(idx) 
            selected_spots.append(slot)

        return selected_spots

    def set_spot(self, x, y, object_type='plant'):
        if isinstance(object_type, int):
            val = object_type

        elif isinstance(object_type, str):
            val = self.OBJECT_TYPES.get(object_type, None)

        self.grid[y,x] = val

    def __repr__(self):
        return f"<World: h={self.height:<4}, w={self.width:<4} | pad thickness={self.padding_thickness:>3}>"
  
    def get_unpadded_grid(self):
        '''return a slice of the main grid excluding the padding margin'''
        pad = self.padding_thickness
        return self.grid[pad:-pad, pad:-pad]

    def get_rgb_img(self):
        '''I'm sleep deprived, so this function might not be very efficient'''
        
        
        if len(self.grid.shape) < 3:
            rgb_grid = np.repeat(self.grid[..., np.newaxis], 3, axis=2)
        
        else:
            rgb_grid = self.grid[:,:,:]
            assert(len(rgb_grid.shape) == 3)

        #print(rgb_grid.shape)
        #----create a 3d vector of the original values (for RGB channels)
        edge_3d      = (self.WORLD_EGDE, ) * 3
        plant_3d     = (self.PLANT,      ) * 3
        herbivore_3d = (self.HERBIVORE,  ) * 3
        carnivore_3d = (self.CARNIVORE,  ) * 3
        omnivore_3d  = (self.OMNIVORE,   ) * 3
        empty_3d     = (self.EMPTY,      ) * 3

        #----Create color masks
        edge_mask      = np.all(rgb_grid==edge_3d,      axis=2)
        plant_mask     = np.all(rgb_grid==plant_3d,     axis=2)
        herbivore_mask = np.all(rgb_grid==herbivore_3d, axis=2)
        carnivore_mask = np.all(rgb_grid==carnivore_3d, axis=2)
        omnivore_mask  = np.all(rgb_grid==omnivore_3d,  axis=2)
        empty_mask     = np.all(rgb_grid==empty_3d,     axis=2)

        #----Apply the masks on the rgb array
        rgb_grid[edge_mask,      :] = self.color_dict[self.WORLD_EGDE]
        rgb_grid[plant_mask,     :] = self.color_dict[self.PLANT]
        rgb_grid[herbivore_mask, :] = self.color_dict[self.HERBIVORE]
        rgb_grid[carnivore_mask, :] = self.color_dict[self.CARNIVORE]
        rgb_grid[omnivore_mask,  :] = self.color_dict[self.OMNIVORE]
        rgb_grid[empty_mask,     :] = self.color_dict[self.EMPTY]
        return rgb_grid

    @property
    def shape(self):
        return (self.height, self.width)

class Simulation(object):
    def __init__(self, 
                 width=500, 
                 height=500, 
                 init_population=50, 
                 max_population=200, 
                 factory=None, 
                 num_generations      = 1,
                 steps_per_generation = 5):

        self.width           = width
        self.height          = height
        self.init_population = init_population
        self.max_population  = max_population
        self.factory         = factory
        self.population      = []
        self.world           = World(width, height)   #initialize empty world

        self.num_gens        = num_generations
        self.spg             = steps_per_generation   #I could make this name more explicit
        self.steps_per_generation = steps_per_generation

    def start(self):
        #----Initialize Population based on parameters
        self.populate_world(self.init_population)
        for gen in range(self.num_gens):
            self.cur_gen = gen  #there might be a more elegant way to keep global track of the timestep and generation number
            print(f"Starting Generation {gen}") if gen % 1 == 0 else None
            for t_step in range(self.steps_per_generation):
                self.cur_t_step = t_step
                print(f"timestep: {t_step} of generation: {gen}") if t_step % 10 == 0 else None
                self.advance_simulation()
        print(f"Ended in Generation {gen}, timestep: {t_step}")

    def populate_world(self, init_population=20):
        '''This will populate the organisms in the world'''
        self.population.clear()
        assert(init_population <= self.max_population)
        assert(init_population <= (self.width * self.height))
        self.world.clear_grids()
        empty_spots = self.world.get_random_empty_spots(init_population)
        #assert(len(empty_spots) == init_population)
        rng = np.random.default_rng()
        for i in range(init_population):
            genome = make_random_genome(num_genes=10, num_brain_connections=15, rng=rng)

            min_x, min_y = 0, 0
            max_x, max_y = self.width, self.height

            #y, x = self.world.get_empty_spot()
            y, x = empty_spots[i]
            org = self.factory.create_organism(genome)   #create new organism
            org.set_pos(x,y)
            self.world.set_spot(x,y, object_type=org.type)
            org.set_pos_boundaries(min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)
            self.population.append(org)

    def advance_simulation(self):
        '''Computes all the changes for the next cycle'''
        for i, org in enumerate(self.population):
            #TODO: get sensor readings from org
            #TODO: perform feedforward propagation of org's neural net
            #TODO: Use output from neural net to perform actions (motions and changes to the environment will be queued to the end of the timestep)

            #TODO: detect collisions between this org and the rest (it might need to work together with the previous step)
            #TODO: apply all world changes at the end of timestep

            #TODO: first detect collisions with every other organism and the environment (create a list of changes to params)
            #remaining_orgs = self.population[:i] + self.population[i+1:]
            collisions     = self.detect_collisions(org, i)
            first_neighbor = collisions[0] if len(collisions) > 0 else org    #get first colliding organism if one is available. If not, choose itself
            sim_params     = {  #package all necessary information in this dictionary so it can be passed to the underlying methods
                'this_org'     : org,
                'neighbor_org' : first_neighbor,
                'steps_per_generation' : self.steps_per_generation,
            }

            #TODO: 
            try:
                actions = org.think(**sim_params)   #make organism think
                perform_actions(actions, org, **sim_params)
            except IndexError as e:
                #print(f"\n{'-'*80}\n{e}")
                print(f"-> Error at generation={self.cur_gen}, timestep={self.cur_t_step}")
                print(f"\n* Index Error (org idx={i}) was caused by Org:\n{org}")
                show_org_info(org)
                print("\n-> Exiting in shame...")
                import sys
                sys.exit()  

    def _advance_simulation(self):
        for i, org in enumerate(self.population):
            colliding_org = self.detect_first_collision(org, i)

            #allow organism to think, based on sensor data

            
    def detect_collisions(self, org, org_idx):
        collisions = []
        for other in self.population[org_idx+1:]:
            #this_x, this_y   = org.get_pos()
            #other_x, other_y = other.get_pos()
            this_pos  = org.get_pos()   #-> (x,y) tuple
            other_pos = other.get_pos() #-> (x,y) tuple

            if this_pos==other_pos:
                collisions.append(other)
        return collisions
    
    #TODO: explore this idea of using a numpy 2D matrix to store the organisms directly.
    def _detect_collisions(self, org, org_idx):
        x, y   = org.get_pos()
        radius = 1
        local_grid = self.world.get_surroundings(x, y, radius)
        
    def detect_first_collision(self, org, org_idx):
        '''Similar to detect_collision, but it returns 
        the first colliding object it finds and ignores the rest.
        It is not a perfect solution, but for now my program can only deal 
        with two organisms interacting at the same time'''
        for other in self.population[org_idx+1:]:
            #this_pos  = org.get_pos()
            #other_pos = other.get_pos()
            #if this_pos == other_pos:
            #    return other
            dist = org.get_distance(other)
            if dist <=1:
                return other
            
        return None  #we only get here if there are no collisions

def sample_run():

    decoders = construct_decoder_directory()
    config = get_settings_from_file()

    num_genes       = 15
    num_brain_conns = 15
    num_senses      = 20
    num_outputs     = 20

    gene_length           = config['phenotype_genome']['gene_length']
    mutation_rate         = config['mutation']['point_mutation_rate']
    gene_duplication_rate = config['mutation']['gene_duplication_rate']
    marker_genes_dict     = config['marker_genes']

    brain_params = config['brain_genome']
    brain_params['num_outputs'] = num_outputs
    brain_params['num_senses']  = num_senses

    pheno_params = config['phenotype_genome']
    pheno_params['gene_decoders'] = decoders

    factory = Factory(gene_length           = gene_length,
                      phenotype_params      = pheno_params,
                      brain_params          = brain_params,
                      marker_genes_dict     = marker_genes_dict,
                      point_mutation_rate   = mutation_rate,
                      gene_duplication_rate = gene_duplication_rate,)


    w = h    = 500
    init_pop = 10
    num_gens = 2
    steps_per_gen = 2

    sim = Simulation(w, h, factory=factory, max_population=10_000, init_population=init_pop, num_generations=num_gens, steps_per_generation=steps_per_gen)
    
    start_t = time.time()
    sim.start()
    end_t   = time.time()

    total_s = end_t - start_t
    
    print(f"\nSimulation completed (Total time: {total_s // 60:.0f} m + {total_s % 60:.2f}s)")
    print(f"\n\t* Generations: {num_gens}\n\t* Steps per generation: {steps_per_gen}")

if __name__ == '__main__':
    from full_factory import Factory
    from tools import get_settings_from_file, make_random_genome
    from decoders import construct_decoder_directory
    from environment import World, Simulation
    import numpy as np
    import matplotlib.pyplot as plt
    import time 

    sample_run()