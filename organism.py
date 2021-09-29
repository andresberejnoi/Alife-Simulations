from matplotlib.pyplot import new_figure_manager
from brain import Brain

from math import sin
from math import cos

class DNA(object):
    def __init__(self):
        self._color_gene        = 0x00
        self._speed_gene        = 0x00
        self._energy_gene       = 0x00
        self._intelligence_gene = 0x00
        self._strength_gene     = 0x00

    @property
    def color_gene(self):
        return self._color_gene
    @property
    def speed_gene(self):
        return self._speed_gene
    @property
    def energy_gene(self):
        return self._energy_gene
    @property
    def intelligence_gene(self):
        return self._intelligence_gene
    @property
    def strength_gene(self):
        return self._strength_gene

class Organism(object):
    def __init__(self):
        self._species_id  = None 
        self._mass        = None   # will be determined by a formula based on area and density or material composition
        self._energy_bar  = None   # some value. this is energy that the organism uses to move and attack and defend
        self._energy_body = None   # energetic value of the organism. Should also be determined based on mass or actual body parameters
        self._dna         = None   # Still not sure how this will be represented
        self._brain       = Brain()   # This will most likely be the neural network controlling the organism
    
        #----Place in the world
        self._xpos        = 0
        self._ypos        = 0
        self._pos         = (self._xpos,self._ypos)   #this might need to be modified

        self._fitness     = 0

    #-------------
    @property
    def species_id(self):
        return self._species_id

    @species_id.setter
    def species_id(self,new_id):
        #add any input checking here before setting the new value
        self._species_id = new_id

    #-------------
    @property
    def mass(self):
        return self._mass

    #-------------
    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self,new_val):
        if new_val < 0:
            self._fitness = 0
        else:
            self._fitness = new_val

    #========================================
    def check_species_compatibility(self, other_dna):
        '''Name could be improved. Check if this species is 
        compatible with `other_dna` species to determine if 
        they belong to the same species'''
        pass

    def compute_fitness(self):
        pass 

    #=======================================
    def __lt__(self,other_org):
        return self.fitness < other_org.fitness

    def __eq__(self, other_org):
        return self.fitness == other_org.fitness   #I'm not sure about this one. I might want to use equality to check if the genome is the same
    
class SimpleOrganism(object):
    def __init__(self):
        # self.genes = ['area', 'num_sides', 'color_r', 
        #               'color_g', 'color_b', 'max_energy',
        #               'max_step']
        self.genes = {
            'radius'     : 0.05,
            'num_sides'  : 6,
            'color_r'    : 200/255,
            'color_g'    : 50/255,
            'color_b'    : 50/255,
            'alpha'      : 1,
            'max_energy' : 50,
            'max_step'   : 0.1
        }
        
        self.gene_expressions = [1, 1, 1, 1, 1, 1, 1]    #binary switches for the different genes in the organisms

        self.brain = Brain()
        self._direction = 90
        self.x_pos = 0
        self.y_pos = 0

        self.energy         = self.genes['max_energy']
        self._age           = 0
        self._dist_traveled = 0

        self.alive  = True 

    def isalive(self):
        return self.alive

    def kill(self):
        self.alive = False 

    def spend_energy(self, amount_to_spend):
        self.energy -= abs(amount_to_spend)
        if self.energy <= 0:
            self.kill()

    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, new_val):
        self._age = abs(new_val)

    @property
    def dist_traveled(self):
        return self._dist_traveled

    @dist_traveled.setter
    def dist_traveled(self, new_val):
        self._dist_traveled = abs(new_val)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_angle):
        '''angles will always remain within [0-360]'''
        if new_angle > 360:
            self._direction = new_angle - 360
        elif new_angle < 0:
            self._direction = new_angle + 360
        else:
            self._direction = new_angle

    def set_position_dir(self, xy_tuple, angle):
        self.x_pos     = xy_tuple[0]
        self.y_pos     = xy_tuple[1]
        self.direction = angle            #this should be the angle of the organism (the direction it is facing)

    def update_coords(self, xy_tuple, angle):
        self.x_pos     += xy_tuple[0]
        self.y_pos     += xy_tuple[1]
        self.direction += angle

    def get_rgb(self):
        return (self.r_color,
                self.g_color,
                self.b_color,)

    def get_rgba(self):
        return (self.r_color,
                self.g_color,
                self.b_color,
                self.alpha,)

    def set_rgba(self,r,g,b,alpha=1):
        self.r_color = r 
        self.g_color = g
        self.b_color = b 
        self.alpha   = alpha

    #-----------
    @property
    def r_color(self):
        return self.genes['color_r']
    
    @r_color.setter
    def r_color(self,new_val):
        if isinstance(new_val,int):
            if new_val >= 0 and new_val <= 255:
                self.genes['color_r'] = new_val/255
            elif new_val < 0:
                self.genes['color_r'] = 0
            elif new_val > 255:
                self.genes['color_r'] = 1

        elif isinstance(new_val,float):
            if new_val >= 0 and new_val <=1:
                self.genes['color_r'] = new_val
            elif new_val < 0:
                self.genes['color_r'] = 0
            elif new_val > 1:
                self.genes['color_r'] = 1

    #-----------
    @property
    def g_color(self):
        return self.genes['color_g']
    
    @g_color.setter
    def g_color(self,new_val):
        if isinstance(new_val,int):
            if new_val >= 0 and new_val <= 255:
                self.genes['color_g'] = new_val/255
            elif new_val < 0:
                self.genes['color_g'] = 0
            elif new_val > 255:
                self.genes['color_g'] = 1

        elif isinstance(new_val,float):
            if new_val >= 0 and new_val <=1:
                self.genes['color_g'] = new_val
            elif new_val < 0:
                self.genes['color_g'] = 0
            elif new_val > 1:
                self.genes['color_g'] = 1
    
    #-----------
    @property
    def b_color(self):
        return self.genes['color_b']
    
    @b_color.setter
    def b_color(self,new_val):
        if isinstance(new_val,int):
            if new_val >= 0 and new_val <= 255:
                self.genes['color_b'] = new_val/255
            elif new_val < 0:
                self.genes['color_b'] = 0
            elif new_val > 255:
                self.genes['color_b'] = 1

        elif isinstance(new_val,float):
            if new_val >= 0 and new_val <=1:
                self.genes['color_b'] = new_val
            elif new_val < 0:
                self.genes['color_b'] = 0
            elif new_val > 1:
                self.genes['color_b'] = 1

    @property
    def alpha(self):
        return self.genes['alpha']

    @alpha.setter 
    def alpha(self, new_val):
        if new_val < 0:
            new_val = 0 
        elif new_val > 1:
            new_val = 1
        
        self.genes['alpha'] = new_val

    #======================================
    def move(self,max_xy, min_xy, outside_inputs=None):
        '''move the organism based on decisions. Returns the amount 
        of distance traveled'''
        inputs = outside_inputs #+ something else, like internal inputs
        step_amount, direction = self.brain.make_decision(inputs)
        total_motion = self.genes['max_step'] * step_amount

        self.direction += direction
        new_xy_pos = [self.x_pos + total_motion*cos(self.direction), self.y_pos + total_motion*sin(self.direction)] 

        #checking that max boundaries are respected
        if new_xy_pos[0] > max_xy[0]:
            new_xy_pos[0] = max_xy[0]
            self.direction = -self.direction
        elif new_xy_pos[0] < min_xy[0]:
            new_xy_pos[0] = min_xy[0]
            self.direction = -self.direction

        if new_xy_pos[1] > max_xy[1]:
            new_xy_pos[1] = max_xy[1]
            self.direction = -self.direction
        elif new_xy_pos[1] < min_xy[1]:
            new_xy_pos[1] = min_xy[1]
            self.direction = -self.direction
            
        self.set_position_dir(new_xy_pos, self.direction)
        self.dist_traveled += total_motion

        return total_motion



class Plant(SimpleOrganism):
    def __init__(self):
        super().__init__()
        self.genes['max_step'] = 0.01    #plants don't move, so this is zero
        self.set_rgba(20/255, 255/255, 50/255, 1)

class Predator(SimpleOrganism):
    def __init__(self):
        super().__init__()
        self.genes['num_sides'] = 3
        self.genes['max_energy'] = 100

