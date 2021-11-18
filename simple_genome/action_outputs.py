import numpy as np

DEFAULT_OUTPUT_ACTIONS = [    #I will treat this array as a brainstorming section
    'secrete_pheromone',
    'motion_magnitude',   #forward distance travel 1 = 100% of possible motion
    'direction_change',
    'set_skin_color_r',
    'set_skin_color_g',
    'set_skin_color_b',
    'set_skin_alpha',
    'set_oscillator',
    'drop_load',
    'pick_up_load',
    'attack_neighbor',
    'reproduce_asexual',
    'reproduce_sexual'
]

def get_num_outputs():
    return len(OUTPUT_ACTIONS)

def get_action_func_by_id(action_id):
    return OUTPUT_ACTIONS[action_id]

def perform_actions(outputs, org, **sim_params):
    """
    outputs: numpy array
        Array of outputs from org's neural network. Values in `outputs`
        can be of any range, so this function will standardize them into a 
        range of 0 to 1 by using a hyperbolic tangent and some divisions.
    org: Organism
        The Organism object that produced the output array
    """
    nnet = org.nnet
    idx_outputs = nnet.active_outputs_idx   #get index of the active outputs

    #active_outputs = outputs[idx_outputs]  #this assumes outputs is a numpy array
    probability_outputs = (np.tanh(outputs) + 1) / 2  #+1 shifts values to [0-2] and the /2 reduces the value in the range [0-1] so it can be used as a probability
    for idx in idx_outputs:
        val = outputs[idx]
        action_func = get_action_func_by_id(idx)
        
        #----Perform the action 
        action_func(org, val, **sim_params)



def secrete_pheromone(org, val, **sim_params):
    pass 

def reproduce_asexual(org, val, **sim_params):
    child_org = None 
    return child_org

def reproduce_sexual(org, val, **sim_params):
    pass 

def set_oscillator(org, val, **sim_params):
    max_t_step = sim_params.get('steps_per_generation')
    #org.oscillator = int((max_t_step * val))
    org.oscillator = min([int(max_t_step*val), max_t_step])

def set_skin_color_r(org, val, **sim_params):     
    color_attr = "temp_rgb"
    if hasattr(org, color_attr):
        temp_rgb   = getattr(org, color_attr)
        new_channel  = min([int(255*val), 255])
        temp_rgb[0] = new_channel 
        setattr(org, color_attr, temp_rgb)

def set_skin_color_g(org, val, **sim_params):
    color_attr = "temp_rgb"
    if hasattr(org, color_attr):
        temp_rgb   = getattr(org, color_attr)
        new_channel  = min([int(255*val), 255])
        temp_rgb[1] = new_channel 
        setattr(org, color_attr, temp_rgb)

def set_skin_color_b(org, val, **sim_params):
    color_attr = "temp_rgb"
    if hasattr(org, color_attr):
        temp_rgb   = getattr(org, color_attr)
        new_channel  = min([int(255*val), 255])
        temp_rgb[2] = new_channel 
        setattr(org, color_attr, temp_rgb)

def set_skin_alpha(org, val, **sim_params):
    attr_name = 'skin_alpha'
    if hasattr(org, attr_name):
        setattr(org, attr_name, val)

#--------MOTION ACTIONS
def change_direction(org, val, **sim_params):
    attr = 'direction'
    if hasattr(org, attr):
        #setattr(org, attr, val)
        original_dir = getattr(org, 'direction')
        val = val * (2*np.pi)  #val will be the amount of angle to rotate (in radians) from current angle
        org_idx = sim_params.get('this_idx')
        
        try:
            motion_vec = sim_params['motion_queue'][org_idx]
        except KeyError:
            motion_vec = [0,0]
            sim_params['motion_queue'][org_idx] = motion_vec

        motion_vec[1] = val
        

def move_by_amount(org, val, **sim_params):
    '''val here represents the strength of motion.
    '''
    #origin = org.get_pos()
    org_idx = sim_params['this_idx']

    try:
        motion_vec = sim_params['motion_queue'][org_idx]
    except KeyError:
        motion_vec = [0,0]
        sim_params['motion_queue'][org_idx] = motion_vec

    motion_vec[0] = 0 if val < 0.5 else 1   #TODO: this line needs to be modified when organisms are able to move more than 1 square
    #sim_params['motion_queue'][0] = 1
    

    


OUTPUT_ACTIONS = [
    set_skin_color_r,
    set_skin_color_g,
    set_skin_color_b,
    set_skin_alpha,
    set_oscillator,
    change_direction,
    move_by_amount,
]