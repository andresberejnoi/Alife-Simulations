import numpy as np
from organism import Organism 
from decoders import EmptyDecoder

class PhenotypeFactory(object):
    def __init__(self,
                 gene_length   = 32,
                 id_length     = 8,
                 switch_length = 1,
                 gene_decoders = None,):  #5 in 1000

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

        #----Objects used inside the code
        self.gene_decoders = gene_decoders
    
    #@classmethod
    def is_gene_on(self, gene):
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

    def create_organism_from_genome(self, genome=[], verbose=False):
        org_attributes = []    #we will be collecting attributes here
        for gene in genome:
            if gene == self.NULL_GENE:
                continue

            is_on = self.is_gene_on(gene)
            if is_on:
                gene_id  = self.get_gene_id(gene)
                gene_val = self.get_gene_val(gene, str_mode=True)  #I'm using string mode to preserve leading zeros, since Python integers will just truncate the bit length until the first 1. I could use fixed-length ints like numpy.uint32 instead
                decoder  = self.gene_decoders.get(gene_id, EmptyDecoder())

                #print(f"Decoding ID:{gene_id} with decoder:\n\t{decoder}")
                org_attributes += decoder.decode(gene_val)
            else:
                continue
        
        #=====================================
        # Here we create the organism with the attributes decoded
        org = Organism()
        for attr in org_attributes:
            setattr(org, attr[0], attr[1])
        return org