from collections import Counter
from default_genes import DEFAULT_GENES
from organism import Organism
import numpy as np

class Gene(object):
    def __init__(self, id=0x0, properties=0x0, value=0x0, is_on=0x1):
        self.id = id
        self.properties = properties
        self.value = value 
        self.is_on = is_on
    
    def __repr__(self):
        return f"<Gene id={self.id}, prop={hex(self.properties)}, val={hex(self.value)}, turned_on={bool(self.is_on)}>"
    
    __str__ = __repr__

class Genome(object):
    '''Genome object
    It keeps track of the gene sequence and can return values from it'''
    #HEADER_LEN = 2    #length of the hex string that represents the header of the gene, from left to right. EX: gene -> 4FFFA9FF, with a header len of 2, the first two characters ('4F') will be used for the gene type
    #GENE_LEN   = 32   #in bits, it will be 
    FULL_GENE_MASK   = 0xFFFFFFFF     # Use to only keep the first 32 bits in a number
    SWITCH_BIT_MASK  = 0x00000001
    HEADER_MASK      = 0x000FFFFF     # .... .... .... 1111 1111 1111 1111 1111
    ID_MASK          = 0x000003FE     # .... .... .... .... .... 0011 1111 1110
    PROPERTIES_MASK  = 0x000FB000     # .... .... .... 1111 1111 1100 0000 0000
    GENE_VALUE_MASK  = 0xFFF00000     # 1111 1111 1111 .... .... .... .... ....

    ID_SHIFT    = 1
    PROP_SHIFT  = 10
    VALUE_SHIFT = 20

    def __init__(self, sequence, split_by='0x'):
        '''
        sequence: iterable of 32 bit numbers, or a string of 32 bit numbers in hex
        split_by: str, optional
            Only used if `sequence` is a string. It is the character or str that will
            be used to split the string into individual numbers. Ex: with `split_by` = '0x'
            the sequence: "0xAA00FFFF0x34561CBA" will turn into an array of ints: [0xAA00FFFF, 0x34561CBA]
        '''
        if isinstance(sequence, str):
            str_genes = sequence.split(split_by)
            self.raw_genes = [(int(gene,16) & self.FULL_GENE_MASK) for gene in str_genes if len(gene) > 0]
            #self.genes = {gene.id:gene for gene in }
        elif isinstance(sequence, list) or isinstance(sequence, tuple):
            self.raw_genes = [(gene & self.FULL_GENE_MASK) for gene in sequence]
            #self.genes_dict = [self.parse_gene(gene) for gene in sequence]
        
        self.genes_dict = self.make_genes_dict()
    #@classmethod
    def parse_gene(self, gene):
        if isinstance(gene,Gene):
            return gene 

        id         = (gene & self.ID_MASK) >> self.ID_SHIFT
        is_on      = (gene & self.SWITCH_BIT_MASK)
        properties = (gene & self.PROPERTIES_MASK) >> self.PROP_SHIFT
        value      = (gene & self.GENE_VALUE_MASK) >> self.VALUE_SHIFT

        g = Gene(id=id, properties=properties, value=value, is_on=is_on)
        return g

    def make_genes_dict(self):
        gene_dict = {}
        for gene in self.raw_genes:
            g = self.parse_gene(gene)
            if g.id in gene_dict:
                gene_dict[g.id].append(g)
            else:
                gene_dict[g.id] = [g]
        return gene_dict

    @classmethod
    def is_same_species(genome_1, genome_2):
        # if isinstance(genome_1, Genome):
        #     pass  # just do stuff here
        # elif isinstance(genome_1, list) or isinstance(genome_1, tuple)
        # if isinstance(genome_2, Genome):
        #     pass  # do other stuff 
        pass 

    def produce_phenotype(self, gene_id_dictionary=DEFAULT_GENES):
        for id in self.genes_dict:
            genes_list = self.genes_dict[id]
            for gene in genes_list:
                if not gene.is_on:
                    continue




    
    def __repr__(self):
        return f"<Genome len={len(self.raw_genes)}>"


class SimpleGene(object):
    def __init__(self, gene, number_base=16):
        if isinstance(gene, str):
            try:
                raw_gene = int(gene, number_base)
            except:
                print(f"Couldn't parse {gene} as int of base {number_base}")
                return None
        elif isinstance(gene, int):
            pass

class EmptyGeneDecoder(object):
    def __init__(self) -> None:
        return None

class SimpleGenome(object):
    def __init__(self, genes, gene_length=32):
        '''
        gene_length: int
            Number of bits per gene. Default is 32
        '''
        self.genes = genes   #Apply some hard organization rule, or something like in nature, where the gene locations have a meaning
        self.gene_length = gene_length
        #self.str_genes = "".join([f"{gene:032b}" for gene in self.genes])

    @property
    def bin_repr(self):
        num_bits = self.gene_length
        return "".join([f"{gene:0{num_bits}b}" for gene in self.genes])

    @property
    def hex_repr(self):
        num_hexes = self.gene_length // 4
        return "".join([f"{gene:0{num_hexes}x}" for gene in self.genes])


def get_full_random_genome(max_genes=20, max_connections=30, gene_length=32):
    genome = []
    genome += get_random_phenotype_genome(max_genes,gene_length)
    genome += get_random_brain_genome(max_connections,gene_length)

    return genome

def get_random_phenotype_genome(max_genes=20, gene_length=32):
    max_val   = int('1'*gene_length, 2) #for 32 bits it will be 0xFFFFFFFF
    data_type = np.__dict__.get(f"np.uint{gene_length}", np.uint32)

    genome = []
    num_genes = np.random.randint(2,max_genes)
    for i in range(num_genes):
        gene = np.random.randint(0,max_val, dtype=data_type)
        genome.append(gene)
    return genome

def get_random_brain_genome(max_connections=25,gene_length=32):
    num_conns = np.random.randint(2,max_connections)
    start_marker = 0x1
    end_marker   = 0x0
    genome = [start_marker]    #start the genome with the brain starter marker

    max_val   = int('1'*gene_length, 2) #for 32 bits it will be 0xFFFFFFFF
    #data_type = np.__dict__.get(f"np.uint{gene_length}", np.uint32)  #get the correct dtype from numpy, or default to np.uint32 if there is no match
    data_type = getattr(np, f"uint{gene_length}", np.uint32)
    for i in range(num_conns):
        if gene_length==32:
            gene = np.random.randint(0,max_val, dtype=data_type)
            genome.append(gene)
        elif gene_length==16:
            for m in range(2):  
                gene = np.random.randint(0,max_val, dtype=data_type)
                genome.append(gene)
        elif gene_length==8:
            for m in range(3):
                gene = np.random.randint(0,max_val, dtype=data_type)
                genome.append(gene)
        else:
            gene = np.random.randint(0, max_val, dtype=data_type)
    genome.append(end_marker)
    return genome

class PhenotypeFactory(object):
    '''Uses a given genome to output an organism with certain characteristics'''
    #Some useful values to make bit masks auto-updating
    GENE_LENGTH    = 32
    ID_LENGTH      = 8   #the number of bits allocated to the id number of the gene
    SWITCH_LENGTH  = 1
    HEADER_LENGTH  = SWITCH_LENGTH + ID_LENGTH

    #Defining Shift length
    ID_SHIFT    = SWITCH_LENGTH
    VALUE_SHIFT = HEADER_LENGTH

    #Create bit masks based on the actual lengths of the gene
    FULL_GENE_MASK  = int('1'*GENE_LENGTH  , 2)             #0xFFFFFFFF     # Use to only keep the first 32 bits in a number
    SWITCH_BIT_MASK = int('1'*SWITCH_LENGTH, 2)                              #0x00000001     # .... .... .... .... .... .... .... ...1
    HEADER_MASK     = int('1'*HEADER_LENGTH, 2)             #0x000007FF     # .... .... .... .... .... .111 1111 1111
    ID_MASK         = HEADER_MASK & ~SWITCH_BIT_MASK        #0x000007FE     # .... .... .... .... .... .111 1111 1110
    #ID_MASK         = int('1'*ID_LENGTH,2) << ID_SHIFT
    GENE_VALUE_MASK = FULL_GENE_MASK & ~HEADER_MASK         #0xFFFFF800     # 1111 1111 1111 1111 1111 1... .... ....

    # #Create bit masks based on the actual lengths of the gene
    # FULL_GENE_MASK   = 0xFFFFFFFF     # Use to only keep the first 32 bits in a number
    # SWITCH_BIT_MASK  = 0x00000001     # .... .... .... .... .... .... .... ...1
    # HEADER_MASK      = 0x000007FF     # .... .... .... .... .... .111 1111 1111
    # ID_MASK          = 0x000007FE     # .... .... .... .... .... .111 1111 1110

    #GENE_VALUE_MASK  = FULL_GENE_MASK & ~HEADER_MASK    #This makes it better adapted to changes in the code
    #GENE_VALUE_MASK  = 0xFFFFF800     # 1111 1111 1111 1111 1111 1... .... ....

    #Special Marker Genes
    NULL_GENE        = 0xAAAAAAAB     # 1010 1010 1010 1010 1010 1010 1010 1011
    START_BRAIN_SEGMENT_GENE = 0x1    # this will work with 8, 16, 32, 64, etc bits
    END_BRAIN_SEGMENT_GENE   = 0x0

    def __init__(self, gene_recipes=None):
        '''
        gene_recipes: dict, or list of tuples, or something
            A dict containing all the possible genes known in this universe,
            along with a default decoder function
        '''
        self.gene_recipes = gene_recipes
        
    @classmethod
    def get_gene_id(cls, gene):
        gene_id = (gene & cls.ID_MASK) >> cls.ID_SHIFT
        return gene_id

    @classmethod
    def is_gene_on(cls, gene):
        if isinstance(gene, Gene):
            return gene.is_on()
        return bool(gene & cls.SWITCH_BIT_MASK)

    def generate_phenotype(self, genes=[], verbose=False):
        '''
        genes: list
            List of genes for generating a particular organism.
        '''
        if isinstance(genes, Genome):
            genes = genes.genes
        
        brain_mode = False
        for gene in genes:
            if gene == self.START_BRAIN_SEGMENT_GENE:
                #Set up the factory to create the brain properly
                brain_mode = True 
                continue
            elif gene == self.END_BRAIN_SEGMENT_GENE:
                brain_mode = False 
                continue

            if brain_mode:
                #Create brain here
                pass 
            else:
                is_on = self.is_gene_on(gene)
                if is_on:
                    gene_id   = self.get_gene_id(gene)
                    gene_decoder =  self.gene_recipes.get(gene_id, EmptyGeneDecoder())
                    gene_name = gene_decoder.name

                    if verbose:
                        print(f"Raw Gene:\n\t* {gene & self.FULL_GENE_MASK:0{self.GENE_LENGTH}b}")
                        print(f"Gene ID: {gene_id}")