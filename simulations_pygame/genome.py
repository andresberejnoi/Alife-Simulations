from collections import Counter
from default_genes import DEFAULT_GENES

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