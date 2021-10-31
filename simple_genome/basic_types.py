from genome import Genome    #It does not look good. I keep importing this into every file. Maybe it should be a basic type

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
        self.output_connections = []
        self.input_connections  = []
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
    def __init__(self, init_xy=(0,0), max_xy=(500,500), min_xy=(-500,-500), genome = []):
        self._max_x, self._max_y = max_xy 
        self._min_x, self._min_y = min_xy 

        self._x_pos, self._y_pos   = init_xy
        self._last_x, self._last_y = init_xy

        #--- Every creature will have a genome
        self._genome = genome
    
    def get_genome(self):
        return self._genome
    
    @property 
    def genome(self):
        return self._genome 
    
    @genome.setter
    def genome(self, genome):
        self._genome = genome

    def set_genome(self, genome):
        #self._genome = [gene for gene in genome]
        self._genome = genome

    def print_genome(self, mode='bin'):
        if mode=='bin':
            print([f"{gene:032b}" for gene in self._genome])
        elif mode=='hex':
            print([f"{gene:08x}" for gene in self._genome])

    @property
    def x_pos(self):
        return self._x_pos

    @x_pos.setter
    def x_pos(self, new_val):
        #new_val = new_val % self._max_x
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
        if new_val > self._max_y:
            new_val = self._min_y + (new_val % self._max_y)
        elif new_val < self._min_y:
            new_val = self._max_y + (new_val % self._min_y)
        self._last_y = self._y_pos
        self._y_pos = new_val
    
    def update_pos(self, x_delta, y_delta):
        '''update organism's position by adding the change in position to current one'''
        self.x_pos += x_delta
        self.y_pos += y_delta

    def set_pos(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

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