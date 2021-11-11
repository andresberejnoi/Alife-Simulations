from genome import Genome    #It does not look good. I keep importing this into every file. Maybe it should be a basic type
import numpy as np
import yaml
#==============================================================================================
# Brain related classes
class Connection(object):
    def __init__(self, source_type, source_id, target_type, target_id, weight) -> None:
        if isinstance(source_type, str):
            self.source_type = source_type
        else:
            self.source_type = 'input' if source_type==0 else 'hidden'
        self.source_id   = source_id

        if isinstance(target_type, str):
            self.target_type = target_type
        else:
            self.target_type = 'hidden' if target_type==0 else 'output'
        self.target_id   = target_id
        self.weight      = weight
    
    def __repr__(self):
        return f"<Conn s_type: {self.source_type:6}, s_id: {self.source_id:3} " +\
               f"| t_type: {self.target_type:6}, t_id: {self.target_id:3}| weight={self.weight:>8}>"
        
    def copy(self):
        return Connection(self.source_type, self.source_id,
                          self.target_type, self.target_id, self.weight)

class Neuron(object):
    def __init__(self, neuron_id=None, neuron_type='',):
        self.type = neuron_type
        self.id   = neuron_id
        self._output = 0.0
        self.num_outputs = 0
        self.num_self_inputs = 0
        self.num_inputs_from_others = 0
        self.remapped_id = 0
        self.driven = True
    
    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, new_val):
        self._output = new_val

    def activate(self):
        pass

    def __repr__(self):
        return f"<Neuron type:{self.type.upper():6}, id:{self.id:>4}, remapped_id:{self.remapped_id:3}, driven={self.driven}>"

#================================================================
# Organism
class BaseOrganism(object):
    def __init__(self, x_pos=0,y_pos=0, max_x=100, max_y=100, min_x=0, min_y=0):
        self._max_x, self._max_y = max_x, max_y 
        self._min_x, self._min_y = min_x, min_y

        self._x_pos, self._y_pos   = x_pos, y_pos
        self._last_x, self._last_y = x_pos, y_pos

        self._next_x = x_pos 
        self._next_y = y_pos
    
    @property
    def max_x(self):
        return self._max_x

    @max_x.setter
    def max_x(self, new_val):
        self._max_x = int(new_val)

    @property
    def max_y(self):
        return self._max_y

    @max_y.setter
    def max_y(self, new_val):
        self._max_y = int(new_val)

    @property
    def min_x(self):
        return self._min_x

    @min_x.setter
    def min_x(self, new_val):
        self._min_x = int(new_val)

    @property
    def min_y(self):
        return self._min_y

    @min_y.setter
    def min_y(self, new_val):
        self._min_y = int(new_val)

    @property 
    def genome(self):
        return self._genome 
    
    @genome.setter
    def genome(self, genome):
        self._genome = genome

    def print_genome(self, mode='bin'):
        if mode=='bin':
            print([f"{gene:032b}" for gene in self._genome])
        elif mode=='hex':
            print([f"{gene:08x}" for gene in self._genome])

    @property   
    def last_x(self):
        return self._last_x

    @property
    def last_y(self):
        return self._last_y

    @property
    def x_pos(self):
        return self._x_pos

    @x_pos.setter
    def x_pos(self, new_val):
        #new_val = new_val % self._max_x
        new_val = int(new_val)
        if new_val > self._max_x:
            new_val = self._min_x + (new_val % self._max_x)
        elif new_val < self._min_x:
            new_val = self._max_x + (new_val % self._min_x)
        self._last_x = self._x_pos
        self._x_pos = new_val
    
    @property
    def y_pos(self):
        return self._y_pos

    #---TODO Fix issues when abs(new_val) > (abs(_max_y) - abs(_min_y))
    @y_pos.setter
    def y_pos(self, new_val):
        new_val = int(new_val)
        if new_val > self._max_y:
            new_val = self._min_y + (new_val % self._max_y)
        elif new_val < self._min_y:
            new_val = self._max_y + (new_val % self._min_y)
        self._last_y = self._y_pos
        self._y_pos = new_val

    @property
    def next_x(self):
        return self._next_x

    @property
    def next_y(self, new_val):
        self._next_x = new_val

    @next_x.setter
    def next_y(self, new_val):
        self._next_y = new_val

    @next_y.setter
    def next_y(self):
        return self._next_y

    @property
    def last_motion_vector(self):
        #new_xy_pos = [self.x_pos + total_motion*cos(self.direction), self.y_pos + total_motion*sin(self.direction)]
        #
        vel = None 
        return vel
    
    @property
    def direction(self):
        '''this is the angle or direction of last motion'''
        # x1, y1 = self.last_x, self.last_y
        # x2, y2 = self.x_pos, self.y_pos
        # mag    = self.motion_magnitude
        # _cos_arg = (x2-x1) / mag
        # direction = np.arccos(_cos_arg)   #inverse cosine: angle = cos^-1((x2-x1)/mag)
        _, _, _, direction = self.get_last_motion_vector()
        return direction

    @property
    def motion_magnitude(self):
        '''Use pythagoream theorem to find magnitude of motion vector from last motion'''
        # x1, y1 = self.last_x, self.last_y
        # x2, y2 = self.x_pos, self.y_pos

        # mag = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        _, _, mag, _ = self.get_last_motion_vector()
        return mag

    def get_last_motion_vector(self):
        x1, y1 = self.last_x, self.last_y
        x2, y2 = self.x_pos, self.y_pos
        
        origin    = (x1, y1)
        dest      = (x2, y2)
        mag       = np.sqrt((x2-x1)**2 + (y2-y1)**2) #vector magnitude
        direction = np.arccos((x2-x1) / mag) 
        #mag       = self.motion_magnitude
        #direction = self.direction
        return (origin, dest, mag, direction)

    def _TODO_get_distance(self, other_org, mode='discrete'):
        '''Finds distance between this org and other_org'''
        if mode=='discrete':
            dist = self._get_discrete_distance(other_org)
        elif mode=='continuous':
            dist = self._get_pythagorean_distance(other_org)
        return dist

    def _get_pythagorean_distance(self, other_org):
        '''returns distance to other_org using Pythagorean's Theorem (for continuous spaces'''
        x1, y1 = self.get_pos()
        x2, y2 = other_org.get_pos()

        dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        #dist = np.linalg.norm(np.array([x1,y1]) - np.array([x2,y2]))
        return dist

    def get_distance(self, other_org):
        '''Computes distance between this and other_org in a discrete 2D grid. 
        All surrounding cells to a cell are a distance of 1, even diagonals'''
        x1, y1 = self.get_pos()
        x2, y2 = other_org.get_pos()

        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return max([dx,dy])

    def update_pos(self, x_delta=0, y_delta=0):
        '''update organism's position by adding the change in position to current one'''
        self.x_pos += x_delta
        self.y_pos += y_delta

    def set_pos(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def set_pos_boundaries(self, min_x, min_y, max_x, max_y):
        self.max_x, self.max_y = max_x, max_y
        self.min_x, self.min_y = min_y, min_y

    def get_pos(self):
        '''returns tuple of (x,y) position (column,row)'''
        return self.x_pos, self.y_pos

    def get_next_pos(self):
        return self.next_x, self.next_y

    def set_next_pos(self, x, y):
        self.next_x = x
        self.next_y = y
    
#==========================================================
# Basic Gene 
class Gene(object):
    pass 

#==========================================================
#  Logging classes

class MutationChange(object):
    def __init__(self, gene_idx=0, original_gene=0, mutation_mask=0, changed_gene=0):
        self.gene_idx      = gene_idx 
        self.original_gene = original_gene
        self.mutation_mask = mutation_mask 
        self.changed_gene  =  changed_gene

    def __repr__(self):
        return f"* Point Mutation at Genome Position: {self.gene_idx:>3}\n\n" +\
               f"\t{self.original_gene:032b} -> original gene\n" +\
               f"\t{self.mutation_mask:032b} -> bits flipped\n"  +\
               f"\t{'|'*32}\n" +\
               f"\t{self.changed_gene:032b} -> result\n"

#===================================================
#---------------Configuration File Class

class ConfigurationSettings(object):
    DEFAULT_FILE = "default_config.yml"
    def __init__(self, config_filename):
        '''
        config_filename: str
            Filename of configuration file (yaml format)    
        '''
        self.filename = config_filename

    def _parse_config_file(self):
        try:
            f_handler = open(self.filename)

        except (FileNotFoundError, TypeError) as e:
            print(f"Given filename `{self.filename}` could not be loaded. Loading default file: `{self.DEFAULT_FILE}`")
            f_handler = open(self.DEFAULT_FILE)

        config = yaml.safe_load(f_handler)
        f_handler.close()