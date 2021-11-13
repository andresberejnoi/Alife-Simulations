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
        Array of outputs from org's neural network
    org: Organism
        The Organism object that produced the output array
    """
    nnet = org.nnet
    idx_outputs = nnet.active_outputs   #get index of the active outputs

    active_outputs = outputs[idx_outputs]  #this assumes outputs is a numpy array

    for idx in idx_outputs:
        val = active_outputs[idx]
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
    org.oscillator = int((max_t_step * val))

def NOT_GOOD_set_skin_color(org, val, color_type='r'):
    color_attr = f"skin_color_{color_type}"
    if hasattr(org, color_attr):
        setattr(org, color_attr) = int(255*val)

def set_skin_color_r(org, val):
    color_attr = "skin_color_r"
    if hasattr(org, color_attr):
        setattr(org, color_attr) = int(255*val)

def set_skin_color_g(org, val):
    color_attr = "skin_color_g"
    if hasattr(org, color_attr):
        setattr(org, color_attr) = int(255*val)

def set_skin_color_b(org, val):
    color_attr = "skin_color_b"
    if hasattr(org, color_attr):
        setattr(org, color_attr) = int(255*val)

def set_skin_alpha(org, val):
    if hasattr(org, 'skin_alpha'):
        org.skin_alpha = val


OUTPUT_ACTIONS = [
    set_skin_color_r,
    set_skin_color_g,
    set_skin_color_b,
    set_skin_alpha,
    set_oscillator,
]