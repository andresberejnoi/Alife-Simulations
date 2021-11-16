"""Define each sensor with a function"""


def get_sensor(sensor_id):
    '''Get sensor reading'''
    return SENSOR_ARRAY[sensor_id]   #people could index SENSOR_ARRAY directly instead of using a function call, but I think this interface is clearer and gives me some flexibility for the future
    
def get_num_senses():
    return len(SENSOR_ARRAY)

def read_sensor(org, input_id, **sim_params):
    sensor = get_sensor(input_id)
    val = sensor(org, **sim_params)
    return val

#-------------LOCATION SENSORS---------------#
def get_current_x(org, **sim_params):
    return org.x_pos

def get_current_y(org, **sim_params):
    return org.y_pos

def get_last_x(org, **sim_params):
    return org.last_x

def get_last_y(org, **sim_params):
    return org.last_y

#-------------COLOR AND APPEARENCES
def get_color_r(org, **sim_params):
    return org.skin_color_r

def get_color_g(org, **sim_params):
    return org.skin_color_g

def get_color_b(org, **sim_params):
    return org.skin_color_b

def get_color_alpha(org, **sim_params):
    return org.skin_alpha

#-------------SURROUNDINGS
def get_biomass_dir_x(org, **sim_params):
    pass 

def get_biomass_dir_y(org, **sim_params):
    pass 

def get_biomass_density(org, **sim_params):
    pass 

#------------Oscillator
def get_oscillator(org, **sim_params):
    return org.oscillator

#-------------NEIGHBOR FUNCTIONS   
# The dir_x, dir_y, and distance functions should work
# to give a vector <x,y> where the distance represents a relative 
# magnitude towards the closest neighbor
#        
def get_genetic_distance(org, **sim_params):
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0

def get_neighbor_direction(org, **sim_params):
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return org.direction

def get_neighbor_dir_x(org, **sim_params):
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
     

def get_neighbor_dir_y(org, **sim_params):
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
     

def get_neihgbor_distance(org, **sim_params):
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
     

def get_neighbor_age(org, **sim_params):
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
     

def get_neighbor_color_r(org, **sim_params):
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
     

def get_neighbor_color_g(org, **sim_params):
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
     

def get_neighbor_color_b(org, **sim_params):
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
        return 0
     

def get_neihgbor_defense(org, **sim_params):
    closest_org = sim_params.get('neighbor_org')
    if org == closest_org:
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
