class Genome(object):
    def __init__(self):
        self.raw_genes       = []
        self.brain_genes     = []
        self.phenotype_genes = []

class Factory(object):
    def __init__(self,
                 gene_length   = 32,
                 id_length     = 8,
                 switch_length = 1,)