"""
Collection of phenotype gene decoders. Right now each decoder is a small class with a `decode` method. 
However, since each class has just one method, it might be better to turn each decoder 
into a simple function and make the code leaner. I will see if the __repr__ method 
provides sufficient advantages to keep the class format.
"""

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

class EmptyDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='Empty'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        return [('empty',True)]

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
        0 -> 000 -> plant
        1 -> 001 -> herbivore
        2 -> 010 -> carnivore
        3 -> 011 -> omnivore
        '''
        if isinstance(gene_value, str):  #assume it is a string representing a binary number (0's and 1's)
            gene_value = int(gene_value, 2)   #the 2 indicates that we want to read this string as a base 2 number (binary)

        possible_types = {
            0: 'plant',
            1: 'herbivore',
            2: 'carnivore',
            3: 'omnivore'
        }
        _type_val = gene_value % len(possible_types)   #this resizes the value so that we always get a valid type
        attrs = [('type', possible_types.get(_type_val, 'plant'))]  #set type from possible type. if it does not exist for some reason, set 'plant' by default
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
        attrs=[('max_speed', 1)]
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
        return attrs

class SkinRGBDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='base_decoder'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        if isinstance(gene_value, str):
            gene_value = int(gene_value, 2)   #in case we get a binary string, convert it back into an int
        blue_mask  = 0xFF
        green_mask = blue_mask << 8
        red_mask   = green_mask << 8

        blue_shift  = 0
        green_shift = 8
        red_shift   = 16

        r = (gene_value & red_mask)   >> red_shift
        g = (gene_value & green_mask) >> green_shift
        b = (gene_value & blue_mask)  >> blue_shift

        attrs = [
            ('skin_color_r', r),
            ('skin_color_g', g),
            ('skin_color_b', b),
        ]
        return attrs

class SkinAlphaDecoder(BaseDecoder):
    def __init__(self, gene_id=None, name='skin_alpha'):
        super().__init__(gene_id=gene_id, name=name)
    def decode(self, gene_value):
        max_val = int('1'*10, 2)    #max possible value on a 24-bit value field (this does not currently check if this bit number is correct. It depends on the Phenotype factory)
        alpha   = min([(gene_value / max_val), 1])   #this will return 1 at most in case the number happens to be higher 

        attrs=[('skin_alpha', alpha)]
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
    SkinRGBDecoder,
    SkinAlphaDecoder,
]

def construct_decoder_directory(decoder_constructors=decoder_constructors):
    gene_decoders = dict()
    for gene_id, constructor in enumerate(decoder_constructors):
        decoder = constructor(gene_id=gene_id)
        gene_decoders[gene_id] = decoder 
    return gene_decoders



