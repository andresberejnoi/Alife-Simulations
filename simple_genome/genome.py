
class Genome(object):
    def __init__(self, genes=[]):
        self.raw_genes   = []
        self.brain_genes = []
        self.pheno_genes = []    #genes that code for physical appearances
        self.genes = dict()

    def 
    def __iter__(self):
        return self 
    def next(self):


class Gene(object):
    pass 

class EmptyGeneDecoder(object):
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

        #Defining Shift length
        self.ID_SHIFT        = self.SWITCH_LENGTH
        self.VALUE_SHIFT     = self.HEADER_LENGTH

        #Create bit masks based on the actual lengths of the gene
        self.FULL_GENE_MASK  = int('1'*self.GENE_LENGTH  , 2)             #0xFFFFFFFF     # Use to only keep the first 32 bits in a number
        self.SWITCH_BIT_MASK = int('1'*self.SWITCH_LENGTH, 2)             #0x00000001     # .... .... .... .... .... .... .... ...1
        self.HEADER_MASK     = int('1'*self.HEADER_LENGTH, 2)             #0x000007FF     # .... .... .... .... .... .111 1111 1111
        self.ID_MASK         = self.HEADER_MASK & ~self.SWITCH_BIT_MASK   #0x000007FE     # .... .... .... .... .... .111 1111 1110
        self.GENE_VALUE_MASK = self.FULL_GENE_MASK & ~self.HEADER_MASK    #0xFFFFF800     # 1111 1111 1111 1111 1111 1... .... ....

        #Special Marker Genes
        self.NULL_GENE                = int('10'*(self.GENE_LENGTH//2), 2)           #0xAAAAAAAA     # 1010 1010 1010 1010 1010 1010 1010 1010
        self.START_BRAIN_SEGMENT_GENE = 0x1                               # this will work with 8, 16, 32, 64, etc bits
        self.END_BRAIN_SEGMENT_GENE   = 0x0

        self.gene_decoders = gene_decoders
    
    @classmethod
    def is_gene_on(cls, gene):
        if isinstance(gene, Gene):
            return gene.is_on()
        return bool(gene & cls.SWITCH_BIT_MASK)

    @classmethod
    def get_gene_id(cls, gene):
        gene_id = (gene & cls.ID_MASK) >> cls.ID_SHIFT
        return gene_id

    def generate_organism(self, genome=[], verbose=False):
        brain_mode = False 
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
                    gene_id      = self.get_gene_id(gene)
                    gene_decoder = self.gene_decoders.get(gene_id, EmptyGeneDecoder)  
                else:
                    continue

