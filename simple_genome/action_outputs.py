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
    'reproduce_asexual',
    'reproduce_sexual'
]

def perform_actions(outputs, org, sim_params={}):
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
        if idx==0:
            set_skin_color(org, val, color_type='r') 
        elif idx==1:
            set_skin_color(org, val, color_type='g')   
        elif idx==2:
            set_skin_color(org, val, color_type='b') 
        elif idx==3:
            set_skin_alpha(org, val)  
        elif idx==4:
            set_oscillator(org, val, max_t_step=sim_params.get('steps_per_generation', 100))  
        elif idx==5:
            pass 
        elif idx==6:
            pass 
        elif idx==7:
            pass 
        elif idx==8:
            pass 
        elif idx==9:
            pass 
        elif idx==10:
            pass 
        elif idx==11:
            pass 
        elif idx==12:
            pass 
        elif idx==13:
            pass 
        elif idx==14:
            pass 
        elif idx==15:
            pass 
        elif idx==16:
            pass 
        elif idx==17:
            pass 
        elif idx==18:
            pass 
        elif idx==19:
            pass 
        elif idx==20:
            pass 



def secrete_pheromone(org, world, val):
    pass 

def reproduce_asexual(org):
    child_org = None 
    return child_org

def reproduce_sexual(this_org, other_org):
    pass 

def set_oscillator(org, val, max_t_step):
    org.oscillator = int((max_t_step * val))

def set_skin_color(org, val, color_type='r'):
    color_attr = f"skin_color_{color_type}"
    if hasattr(org, color_attr):
        setattr(org, color_attr) = int(255*val)

def set_skin_alpha(org, val):
    if hasattr(org, 'skin_alpha'):
        org.skin_alpha = val


    