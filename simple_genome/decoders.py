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
        return [('empty',True)]

    def __repr__(self):
        return f"<Decoder for Gene {self.name}, id={self.id}>"

class EmptyDecoder(BaseDecoder):
    pass 

class EyeDecoder(BaseDecoder):
    def __init__(self, gene_id, name='Eye'):
        super().__init__(gene_id, name)
    def decode(self, gene_value):
        attrs = [('sensor_r',1), ('sensor_g',1), ('sensor_b',1), ('vision_distance',5)]
        return attrs

class EarDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='Ear'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        attrs=[('hearing_distance',5)]
        return attrs

class NoseDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='Nose'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        attrs=[('smelling_distance',5)]
        return attrs

class StomachDecoder(BaseDecoder):
    def __init__(self, gene_id, name='Stomach'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
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
    def decode(self, gene_value):
        attrs=[('lung_type',0), ('lung_capacity',100)]
        return attrs
    
class SpeedDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='Speed'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        attrs=[('max_speed', 100)]
        return attrs

class GrowthDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='growth_rate'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        attrs=[('growth_rate',50)]
        return attrs

class SizeDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='Size'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        attrs=[('max_size',20)]
        return attrs

class PheromoneDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='pheromone'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        '''pheromone_channel -> can be 0, 1, 2 (corresponding to r,g,b'''
        attrs=[('pheromone_strength',10), ('pheromone_channel',0)]

class SkinColorRedDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='skin_color_red'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        attrs=[('skin_color_r',255)]
        return attrs

class SkinColorGreenDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='skin_color_green'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        attrs=[('skin_color_g',255)]
        return attrs

class SkinColorBlueDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='skin_color_blue'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        attrs=[('skin_color_b',255)]
        return attrs

class SkinAlphaDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='skin_alpha'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        attrs=[('skin_alpha',1.0)]
        return attrs

decoder_constructors = [ 
    EyeDecoder,
    EarDecoder,
    NoseDecoder,
    PheromoneDecoder,
    StomachDecoder,
    LungDecoder,
    SpeedDecoder,
    GrowthDecoder,
    SizeDecoder,
    SkinColorRedDecoder,
    SkinColorGreenDecoder,
    SkinColorBlueDecoder,
    SkinAlphaDecoder,

]

def construct_decoder_directory(decoder_constructors=decoder_constructors):
    gene_decoders = dict()
    for gene_id, constructor in enumerate(decoder_constructors, 2):
        decoder = constructor(gene_id=gene_id)
        gene_decoders[gene_id] = decoder 
    return gene_decoders



