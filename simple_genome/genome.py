
from collections import UserList

class Genome(UserList):
    '''Subclasses a safe list-like object.
    This class might be unnecessary. I just created
    to have the nice __repr__ method easily
    accessible, but if it makes the program too slow, it
    should go away.'''
    def __init__(self, genes=[], gene_length=32):
        super().__init__(genes)
        self.gene_length = 32

    # def __repr__(self):
    #     return f"<Genome: num_genes={len(self):>3} | gene_length={self.gene_length:>3}-bit>"

    def __repr__(self):
        return "\n".join([f"{gene:0{self.gene_length}b}" for gene in self])

