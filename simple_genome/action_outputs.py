import numpy as np

DEFAULT_OUTPUT_ACTIONS = [
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
    'reproduce',
]

def perform_actions(outputs, org):
    """
    outputs: numpy array
        Array of outputs from org's neural network
    org: Organism
        The Organism object that produced the output array
    """
    idx_outputs = np.where(outputs != 0)


def secrete_pheromone(org, world, val):
    pass 

def reproduce(org):
    child_org = None 
    return child_org

def set_oscillator(org, val, max_t_step):
    org.oscillator = int((max_t_step * val))

def set_skin_color(org, val, color_type='r'):
    color_attr = f"skin_color_{color_type}"
    if hasattr(org, color_attr):
        setattr(org, color_attr) = int(255*val)

def set_skin_alpha(org, val):
    if hasattr(org, 'skin_alpha'):
        org.skin_alpha = val


    