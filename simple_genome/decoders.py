from default_genes import DEFAULT_GENES

class BaseDecoder(object):
    def __init__(self, gene_id=None, name='base_decoder'):
        self.name = name
        self.id   = gene_id

    def decode(self, gene_value):
        '''
        OVERRIDE THIS METHOD.
        Takes a `gene_value` (fixed length int) and decodes it into attributes
        for an organism. `gene_value` should be the part of the gene after
        removing all switch and id bits. For instance, in a 32-bit gene encoding
        where the ID takes 8 bits and the switch is 1 bit, `gene_value` should
        be an unsigned int with 23 bits. It gets kind of funky dealing with 
        ints and bits in Python, but it is what it is right now.
        
        Returns
        -------
        List of tuples. Each tuple contains an attribute name and its value.
        '''
    def __repr__(self):
        return f"<Decoder for Gene {self.name}, id={self.id}>"


class EyeDecoder(BaseDecoder):
    def __init__(self, gene_id, name='Eye'):
        super().__init__(gene_id, name)
    def decode(self, gene_value):
        attrs = [('sensor_r',1), ('sensor_g',1), ('sensor_b',1)]
        return attrs

class StomachDecoder(BaseDecoder):
    def __init__(self, gene_id, name='Stomach'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self,gene_value):
        '''
        0 -> 000 -> sunlight
        1 -> 001 -> plant
        2 -> 010 -> meat
        3 -> 011 -> omnivore
        4 -> 100 -> everything
        '''
        attrs = [('food_type','omnivore')]
        return attrs

class LungDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='Lung'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self,gene_value):
        attrs=[('lung_type',0), ('lung_capacity',100)]
        return attrs
    
class SpeedDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='Speed'):
        super().__init__(gene_id=gene_id, name=name)
    def decoder(self, gene_value):
        attrs=[('max_speed', 100)]
        return attrs

class GrowthDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='Growth'):
        super().__init__(gene_id=gene_id, name=name)
    def decoder(self, gene_value):
        attrs=[('growth_rate',50)]
        return attrs

class PheromoneDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='Pheromone'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        attrs=[]

class SkinDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='Base Skin'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        attrs=[]
        return attrs

decoder_constructors = [ 
    EyeDecoder,
    PheromoneDecoder
]

def construct_decoder_directory(default_genes=DEFAULT_GENES):
    gene_decoders = dict()
    for gene_id in default_genes:
        decoder = 
        gene_decoders[gene_id]


