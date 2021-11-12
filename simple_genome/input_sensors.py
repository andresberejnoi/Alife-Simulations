"""Define each sensor with a function"""

def get_sensor(sensor_id):
    if sensor_id==0:
        return get_current_x
    elif sensor_id==1:
        return get_current_y
    elif sensor_id==2:
        return get_last_x
    elif sensor_id==3:
        return get_last_y
    elif sensor_id==4:
        return get_color_r
    elif sensor_id==5:
        return get_color_g
    elif sensor_id==6:
        return get_color_b
    elif sensor_id==7:
        return get_color_alpha

    #--------Neighbor related sensors
    elif sensor_id==8:
        return get_genetic_distance
    elif sensor_id==9:
        return get_neihgbor_distance
    

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



