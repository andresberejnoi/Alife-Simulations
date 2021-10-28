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
    
    @property
    def x_pos(self):
        return self._x_pos

    @x_pos.setter
    def x_pos(self, new_val):
        self._last_x = self._x_pos
        self._x_pos = new_val
    
    @property
    def y_pos(self):
        return self._y_pos

    @y_pos.setter
    def y_pos(self, new_val):
        self._last_y = self._y_pos
        self._y_pos = new_val


class Organism(object):
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

    #@classmethod
    def get_gene_id(self, gene):
        gene_id = (gene & self.ID_MASK) >> self.ID_SHIFT
        return gene_id
    
    #@classmethod
    def get_gene_val(self, gene, str_mode=True):
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

#===========================
class Neuron(object):
    def __init__(self, neuron_id, neuron_type='hidden', connections=[], activation_func=np.tanh):
        self.type        = neuron_type
        self.id          = neuron_id
        self.connections = connections
        if self.type.lower()=='input':
            self.activation_func = lambda x: x
        else:  #hidden and output neurons have the same activation, but this can be easily changed
            self.activation_func = activation_func
        
        self.accum_input = 0   #accumulated inputs from the previous connections
    
    def accumulate_input(self, input_val):
        self.accum_input += input_val

    def activate(self, input_val=0):
        self.accum_input += input_val
        activated_input = self.activation_func(self.accum_input)
        if self.type=='output':
            return activated_input

        for conn,weight in zip(self.connections, self.weights):
            output = activated_input * weight
            conn.accumulate_input(output)

def apply_mask(val, mask, left_shift=0):
    return (val & mask) >> left_shift

def create_brain(genome, weight_div_constant=10_000):
    SOURCE_LAYER_ID_MASK    = 0x80000000
    SOURCE_LAYER_ID_SHIFT   = 31

    SOURCE_NEURON_ID_MASK   = 0x7f000000
    SOURCE_NEURON_ID_SHIFT  = 24

    TARGET_LAYER_ID_MASK   = 0x00800000
    TARGET_LAYER_ID_SHIFT  = 23

    TARGET_NEURON_ID_MASK  = 0x007f0000
    TARGET_NEURON_ID_SHIFT = 16
    
    WEIGHT_MASK            = 0x0000ffff
    WEIGHT_SHIFT           = 0
    neurons = {'inputs':[], 'hidden':[], 'outputs':[]}
    unique_neurons = []
    for gene in genome:
        source_type = apply_mask(gene, SOURCE_LAYER_ID_MASK, SOURCE_LAYER_ID_SHIFT)
        source_id   = apply_mask(gene, SOURCE_NEURON_ID_MASK, SOURCE_NEURON_ID_SHIFT)

        target_type = apply_mask(gene, TARGET_LAYER_ID_MASK, TARGET_LAYER_ID_SHIFT)
        target_id   = apply_mask(gene, TARGET_NEURON_ID_MASK, TARGET_NEURON_ID_SHIFT)

        _weight     = apply_mask(gene, WEIGHT_MASK, WEIGHT_SHIFT)
        weight      = _weight / weight_div_constant   #make the weight a small value between -3.2 to 3.0

        
        if source_type==0:     #input layer
            source_layer = 'inputs' 
        else:                  #hidden layer
            source_layer = 'hidden' 

        if target_type==0:     #hidden layer
            target_layer = 'hidden' 
        else:                  #output layer
            target_layer = 'outputs' 

        neurons[source_layer].append(source_id)
        neurons[target_layer].append(target_id)

        neuron = Neuron()
