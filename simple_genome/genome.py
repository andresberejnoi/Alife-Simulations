import numpy as np
from numpy import random
from decoders import EmptyDecoder
from brain import BrainFactory

from collections import UserList

class Genome(UserList):
    '''Subclasses a safe list-like object'''
    def __init__(self, genes=[], gene_length=32):
        super().__init__(genes)
        self.gene_length = 32

    # def __repr__(self):
    #     return f"<Genome: num_genes={len(self):>3} | gene_length={self.gene_length:>3}-bit>"

    def __repr__(self):
        return "\n".join([f"{gene:0{self.gene_length}b}" for gene in self])


class BaseOrganism(object):
    def __init__(self, init_xy=(0,0), max_xy=(500,500), min_xy=(-500,-500), genome = []):
        self._max_x, self._max_y = max_xy 
        self._min_x, self._min_y = min_xy 

        self._x_pos, self._y_pos   = init_xy
        self._last_x, self._last_y = init_xy

        #--- Every creature will have a genome
        self._genome = [gene for gene in genome]
    
    def get_genome(self):
        return self._genome

    def set_genome(self, genome):
        self._genome = [gene for gene in genome]

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

class Organism(BaseOrganism):
    pass 

class Gene(object):
    pass 

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
               f"\t{'-'*32}\n" +\
               f"\t{self.changed_gene:032b} -> result"

class Factory(object):
    def __init__(self,
                 gene_length   = 32,
                 id_length     = 8,
                 switch_length = 1,
                 gene_decoders = None, brain_factory=None,
                 mutation_rate = 0.01,   #1 in 100
                 duplication_error_rate = 0.005):  #5 in 1000

        self.GENE_LENGTH     = gene_length
        self.ID_LENGTH       = id_length   #the number of bits allocated to the id number of the gene
        self.SWITCH_LENGTH   = switch_length
        self.HEADER_LENGTH   = self.SWITCH_LENGTH + self.ID_LENGTH
        self.VALUE_LENGTH    = self.GENE_LENGTH - self.HEADER_LENGTH

        #Defining Shift length
        self.ID_SHIFT        = self.SWITCH_LENGTH
        self.VALUE_SHIFT     = self.HEADER_LENGTH

        #Create bit masks based on the actual lengths of the gene
        self.FULL_GENE_MASK  = int('1'*self.GENE_LENGTH  , 2)                #0xFFFFFFFF     # Use to only keep the first 32 bits in a number
        self.SWITCH_BIT_MASK = int('1'*self.SWITCH_LENGTH, 2)                #0x00000001     # .... .... .... .... .... .... .... ...1
        self.HEADER_MASK     = int('1'*self.HEADER_LENGTH, 2)                #0x000001FF     # .... .... .... .... .... ...1 1111 1111
        self.ID_MASK         = self.HEADER_MASK    & ~self.SWITCH_BIT_MASK   #0x000001FE     # .... .... .... .... .... ...1 1111 1110
        self.GENE_VALUE_MASK = self.FULL_GENE_MASK & ~self.HEADER_MASK       #0xFFFFFE00     # 1111 1111 1111 1111 1111 111. .... ....

        #Special Marker Genes
        self.NULL_GENE                = int('10'*(self.GENE_LENGTH//2), 2)   #0xAAAAAAAA     # 1010 1010 1010 1010 1010 1010 1010 1010
        self.START_BRAIN_SEGMENT_GENE = 0x1                               # this will work with 8, 16, 32, 64, etc bits
        self.END_BRAIN_SEGMENT_GENE   = 0x0

        self.marker_genes = [self.NULL_GENE, self.START_BRAIN_SEGMENT_GENE, self.END_BRAIN_SEGMENT_GENE]

        #Mutation Rates and related values
        self.mutation_rate = mutation_rate
        self.duplication_error_rate = duplication_error_rate
        #----Objects used inside the code
        self.gene_decoders = gene_decoders
        self.brain_factory = brain_factory
        self._set_up_point_mutation_masks()
    
    #@classmethod
    def is_gene_on(self, gene):
        if isinstance(gene, Gene):
            return gene.is_on()
        return bool(gene & self.SWITCH_BIT_MASK)

    def renumber_gene_id(self, original_id):
        return original_id % len(self.gene_decoders)  #the gene id will always be between 0 and the total number of available genes

    #@classmethod
    def get_gene_id(self, gene):
        gene_id = (gene & self.ID_MASK) >> self.ID_SHIFT
        gene_id = self.renumber_gene_id(gene_id)    #I don't need this function call. It could be done in one line here, but I will keep it for now, so as to separate those processes just in case
        return gene_id
    
    #@classmethod
    def get_gene_val(self, gene, str_mode=True, astype=None):
        gene_val = (gene & self.GENE_VALUE_MASK) >> self.VALUE_SHIFT
        if str_mode:
            gene_val = f"{gene_val:0{self.VALUE_LENGTH}b}"    #converts gene int into str, with leading zeros if necessary to maintain the appropriate length
        return gene_val

    def generate_organism(self, genome=[], verbose=False):
        brain_mode = False 
        org_attributes = []    #we will be collecting attributes here
        brain_genome = []
        for gene in genome:
            if gene == self.START_BRAIN_SEGMENT_GENE:
                brain_mode = True 
                continue
            elif gene == self.END_BRAIN_SEGMENT_GENE:
                brain_mode = False
                continue
            elif gene ==  self.NULL_GENE:
                continue

            if brain_mode:
                brain_genome.append(gene)
            else:
                is_on = self.is_gene_on(gene)
                if is_on:
                    gene_id  = self.get_gene_id(gene)
                    gene_val = self.get_gene_val(gene, str_mode=True)  #I'm using string mode to preserve leading zeros, since Python integers will just truncate the bit length until the first 1. I could use fixed-length ints like numpy.uint32 instead
                    decoder  = self.gene_decoders.get(gene_id, EmptyDecoder())

                    print(f"Decoding ID:{gene_id} with decoder:\n\t{decoder}")
                    org_attributes += decoder.decode(gene_val)
                else:
                    continue
        
        #=====================================
        # Here we create the organism with the attributes decoded
        org = Organism(genome = genome)
        for attr in org_attributes:
            setattr(org, attr[0], attr[1])


        #here we create the neural network for the organism
        nnet = self.brain_factory.create_wiring_from_genome(brain_genome)
        org.nnet = nnet 
        return org

    #===========================MUTATION FUNCTIONS 
    def apply_point_mutations(self, genome, num_mutations=1, num_flips=1, use_genome_copy=False, protect_guards=True):
        '''Randomly applies a mutation masks to a random gene or genes'''
        if use_genome_copy:
            genome = [gene for gene in genome]    #this local variable will reference a copy of the passed list

        if num_flips=='random':
            num_flips = np.random.randint(0, self.GENE_LENGTH)
        
        len_genome = len(genome)
        changes = []
        for i in range(num_mutations):
            rnd_gene_idx = np.random.randint(0, len_genome)
            mutation_mask = self._get_composite_mutation_mask(num_flips)

            #_change = [rnd_gene_idx, genome[rnd_gene_idx]]
            _change = MutationChange(gene_idx=rnd_gene_idx, original_gene=genome[rnd_gene_idx])
            if protect_guards:
                while genome[rnd_gene_idx] in self.marker_genes:
                    rnd_gene_idx = np.random.randint(0, len_genome)   #keep getting a new idx until it is not a marker gene

            genome[rnd_gene_idx] ^= mutation_mask   #this flips the bit or bits


            _change.mutation_mask = mutation_mask
            _change.changed_gene  = genome[rnd_gene_idx]

            changes.append(_change)
        return genome, changes

    def _get_composite_mutation_mask(self,num_flips=1):
        '''Create a mutation mask that can have 1 or more genes flipped.'''
        mutation_mask = 0
        for i in range(num_flips):
            random_shift = np.random.randint(0, self.GENE_LENGTH)
            bit_to_flip = self._point_mutation_masks[random_shift]
            mutation_mask = mutation_mask | bit_to_flip
        return mutation_mask

    def _set_up_point_mutation_masks(self):
        self._point_mutation_masks = []
        shifting_mask = 0x1
        for i in range(self.GENE_LENGTH):
            self._point_mutation_masks.append(shifting_mask << i)

    
    def apply_gene_duplication_error(self):
        pass 
            

def OLD_create_random_genome(max_gene_id=15, num_genes=30, gene_length=32, id_length=8, switch_length=1):
    data_type  = getattr(np, f"uint{gene_length}", np.uint32)
    uint_maker = data_type
    
    max_val = int('1'*gene_length,2)   #0xffffffff
    genome  = np.random.randint(max_val, size=num_genes, dtype=data_type)

    mask = ~uint_maker(int('1'*id_length,2) << switch_length)
    #mask = uint_maker(0xfffffe01)    #if bit_length is 32, then this is like doing np.uint32(0x....)
    restricted_ids = np.random.randint(2, max_gene_id, size=num_genes, dtype=data_type)
    genome         = (genome & mask) | restricted_ids
    return genome

def create_random_genome(num_genes=30, gene_length=32):
    data_type = getattr(np, f"uint{gene_length}", np.uint32)
    low       = np.iinfo(data_type).min
    high      = np.iinfo(data_type).max

    genome    = np.random.randint(low, high, size=num_genes, dtype=data_type)
    return list(genome)
