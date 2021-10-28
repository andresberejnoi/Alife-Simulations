"""Define each sensor with a function"""


#-------------LOCATION SENSORS---------------#
def get_current_x(org):
    return org.x_pos

def get_current_y(org):
    return org.y_pos

def get_last_x(org):
    return org.last_x

def get_last_y(org):
    return org.last_y

#-------------COLOR AND APPEARENCES
def get_color_r(org):
    return org.color_r

def get_color_g(org):
    return org.color_g

def get_color_b(org):
    return org.color_b

def get_color_alpha(org):
    return org.color_alpha

#-------------SURROUNDINGS
def get_biomass_dir_x(org):
    pass 

def get_biomass_dir_y(org):
    pass 

def get_biomass_density(org):
    pass 


#-------------NEIGHBOR FUNCTIONS   
# The dir_x, dir_y, and distance functions should work
# to give a vector <x,y> where the distance represents a relative 
# magnitude towards the closest neighbor
#        
def get_genetic_distance(org1, org2):
    pass 

def get_neighbor_dir_x(org):
    pass 

def get_neighbor_dir_y(org):
    pass 

def get_neihgbor_distance(org):
    pass 

def get_neighbor_age(org):
    pass 

def get_neighbor_color_r(org):
    pass 

def get_neighbor_color_g(org):
    pass 

def get_neighbor_color_b(org):
    pass 

def get_neihgbor_defense(org):
    pass 



