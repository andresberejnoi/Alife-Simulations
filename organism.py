class DNA(object):
    def __init__(self):
        self._color_gene        = 0x00
        self._speed_gene        = 0x00
        self._energy_gene       = 0x00
        self._intelligence_gene = 0x00
        self._strength_gene     = 0x00

    @property
    def color_gene(self):
        return self._color_gene
    @property
    def speed_gene(self):
        return self._speed_gene
    @property
    def energy_gene(self):
        return self._energy_gene
    @property
    def intelligence_gene(self):
        return self._intelligence_gene
    @property
    def strength_gene(self):
        return self._strength_gene

class Organism(object):
    def __init__(self):
        self._species_id  = None 
        self._mass        = None   # will be determined by a formula based on area and density or material composition
        self._energy_bar  = None   # some value. this is energy that the organism uses to move and attack and defend
        self._energy_body = None   # energetic value of the organism. Should also be determined based on mass or actual body parameters
        self._dna         = None   # Still not sure how this will be represented
        self._brain       = None   # This will most likely be the neural network controlling the organism
    
        #----Place in the world
        self._xpos        = 0
        self._ypos        = 0
        self._pos         = (self._xpos,self._ypos)   #this might need to be modified

        self._fitness     = 0

    #-------------
    @property
    def species_id(self):
        return self._species_id

    @species_id.setter
    def species_id(self,new_id):
        #add any input checking here before setting the new value
        self._species_id = new_id

    #-------------
    @property
    def mass(self):
        return self._mass

    #========================================
    def check_species_compatibility(self,other_dna):
        '''Name could be improved. Check if this species is 
        compatible with `other_dna` species to determine if 
        they belong to the same species'''
        pass

    
class SimpleOrganism(object):
    def __init__(self):
        self.genes = ['area', 'num_sides', 'color_r', 
                      'color_g', 'color_b', 'max_energy',
                      'max_step']