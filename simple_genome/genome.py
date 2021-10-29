import numpy as np
from decoders import EmptyDecoder

class Genome(object):
    def __init__(self, genes=[]):
        self.raw_genes   = []
        self.brain_genes = []
        self.pheno_genes = []    #genes that code for physical appearances
        self.genes = dict()

    def __iter__(self):
        return self 
    def next(self):
        pass 

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

class Factory(object):
    def __init__(self,
                 gene_length   = 32,
                 id_length     = 8,
                 switch_length = 1,
                 gene_decoders = None):

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

        self.gene_decoders = gene_decoders
    
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
                pass 
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
        org = Organism()
        for attr in org_attributes:
            setattr(org, attr[0], attr[1])

        return org


def create_random_genome(max_gene_id=15, num_genes=30, gene_length=32, id_length=8, switch_length=1):
    data_type = getattr(np, f"uint{gene_length}", np.uint32)
    uint_maker = data_type
    
    max_val = int('1'*gene_length,2)   #0xffffffff
    genome = np.random.randint(max_val, size=num_genes, dtype=data_type)

    mask = ~uint_maker(int('1'*id_length,2) << switch_length)
    #mask = uint_maker(0xfffffe01)    #if bit_length is 32, then this is like doing np.uint32(0x....)
    restricted_ids = np.random.randint(2, max_gene_id, size=num_genes, dtype=data_type)
    genome = (genome & mask) | restricted_ids
    return genome

