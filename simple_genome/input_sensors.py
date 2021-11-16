"""Define each sensor with a function"""


def get_sensor(sensor_id):
    '''Get sensor reading'''
    return SENSOR_ARRAY[sensor_id]   #people could index SENSOR_ARRAY directly instead of using a function call, but I think this interface is clearer and gives me some flexibility for the future
    
def get_num_senses():
    return len(SENSOR_ARRAY)

def read_sensor(input_id, **sim_params):
    sensor = get_sensor(input_id)
    val = sensor(**sim_params)
    return val

#-------------LOCATION SENSORS---------------#
def get_current_x(**sim_params):
    org = sim_params.get('this_org')
    return org.x_pos

def get_current_y(**sim_params):
    org = sim_params.get('this_org')
    return org.y_pos

def get_last_x(**sim_params):
    org = sim_params.get('this_org')
    return org.last_x

def get_last_y(**sim_params):
    org = sim_params.get('this_org')
    return org.last_y

#-------------COLOR AND APPEARENCES
def get_color_r(**sim_params):
    org = sim_params.get('this_org')
    return org.skin_color_r

def get_color_g(**sim_params):
    org = sim_params.get('this_org')
    return org.skin_color_g

def get_color_b(**sim_params):
    org = sim_params.get('this_org')
    return org.skin_color_b

def get_color_alpha(**sim_params):
    org  = sim_params.get('this_org')
    return org.skin_alpha

#-------------SURROUNDINGS
def get_biomass_dir_x(**sim_params):
    org = sim_params.get('this_org')
    pass 

def get_biomass_dir_y(**sim_params):
    org = sim_params.get('this_org')
    pass 

def get_biomass_density(**sim_params):
    org = sim_params.get('this_org')
    pass 

#------------Oscillator
def get_oscillator(**sim_params):
    org = sim_params.get('this_org')
    return org.oscillator

#-------------NEIGHBOR FUNCTIONS   
# The dir_x, dir_y, and distance functions should work
# to give a vector <x,y> where the distance represents a relative 
# magnitude towards the closest neighbor
#        
def get_genetic_distance(**sim_params):
    org         = sim_params.get('this_org')
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
    else:
        return 1

def get_neighbor_direction(**sim_params):
    org         = sim_params.get('this_org')
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return org.direction
    
    return 0

def get_neighbor_dir_x(**sim_params):
    org         = sim_params.get('this_org')
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
    return 0

def get_neighbor_dir_y(**sim_params):
    org         = sim_params.get('this_org')
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
    return 0
     

def get_neihgbor_distance(**sim_params):
    org         = sim_params.get('this_org')
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
    return 0
    

def get_neighbor_age(**sim_params):
    org         = sim_params.get('this_org')
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
    return 0
     

def get_neighbor_color_r(**sim_params):
    org         = sim_params.get('this_org')
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
    return 0
     

def get_neighbor_color_g(**sim_params):
    org         = sim_params.get('this_org')
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
    return 0
     

def get_neighbor_color_b(**sim_params):
    org         = sim_params.get('this_org')
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
    return 0
     

def get_neihgbor_defense(**sim_params):
    org         = sim_params.get('this_org')
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
    return 0
     


#-------Convenient array of sensor functions
SENSOR_ARRAY = [
    get_current_x,
    get_current_y,
    get_last_x,
    get_last_y,
    get_color_r,
    get_color_g,
    get_color_b,
    get_color_alpha,
    get_oscillator,

    #---Sensors dealing with another organism
    get_genetic_distance,
    get_neihgbor_distance,
    get_neighbor_dir_x,
    get_neighbor_dir_y,

    
]
