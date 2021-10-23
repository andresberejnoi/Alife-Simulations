gene_names = [
    'stomach_type',
    'lung_type',

    #Interactions with the environment (sensors)
    'eye', 'eye_type',
    'ear',
    'nose',
    'pheromone',    #controls type and emission of pheromones to leave messages 
    'memory',    #controls whether the organism has some memory and how it is arranged. Memory can be used to keep temporary values
    'data_output',   #controls the ability of this organism to transmit data into its surroundings, so it can be picked up by others
    #'brain',    #Not sure how to handle this yet, but it should control the basic setup for a neural network of some sort, or basic reactions to stimuli

    'speed',   #controls max speed for the organism
    'energy_storage', 'metabolic_rate',  #metabolic rate determines how quickly an organism loses energy but also how much energy the organism can use in a single operation. i.e. a high metabolic rate will allow the organism to engage in high energy activities, like running and chasing prey. A low rate will allow the organism to be more energy efficient and move more slowly, like a snail
    'size',
    'growth_rate',  #the speed at which the organism reaches maturity
    'density',  #density might not be necessary since there is a material_type attribute
    'density_type' ,#Density type can be used to describe the distribution of mass in the body (Gaussian, normal, )
    
    'surface_type', 'skin_color_r', 'skin_color_g', 'skin_color_b', 'skin_color_alpha',  #surface type could be furry, scaled, skin, etc, and maybe striped. Then each stripe would be associated with its own color genes

    #Limbs and Stuff about the body
    'leg', 'tail', 'wing', 'claw', #claw could be changed to a better name. It is supposed to be a weapon
    'joint', #controls the number of joints in the body. 
    'material_type',  #material type is the type of material the body is made of (it will affect the density). Density type can be used to describe the distribution of mass in the body (Gaussian, normal, )
    'basic_shape',  #controls the basic shape of the organism (circle, square, rectangular, star)
    
    #Behavior
    'fear', 'altruism', 'collaboration', 'clinginess'



]

#I'm numbering the genes automatically because I'm lazy to designate a specific number for each
DEFAULT_GENES ={
    i:gene_name for i,gene_name in enumerate(gene_names)
}

#Some of the basic input neurons were taken from David Randall Miller's video here:
# https://www.youtube.com/watch?v=N3tRFayqVtk&t=668s

#the sensory inputs could be specific to only the front of the creature, or maybe I'll just keep it general to any side for now
DEFAULT_INPUT_NEURONS = [
    'pheromone_level',
    'pheromone_dir_x',
    'pheromone_dir_y',
    'attack_power',
    'age',
    'color_r',
    'color_g',
    'color_b',
    'last_x',
    'last_y',
    'current_x',
    'current_y',
    'biomass_density',   #equivalent to population density from the video linked above, but I think I like Biomass better. I might change it
    'biomass_dir_x',     #direction in x towards greatest biomass
    'biomass_dir_y',     
    'oscillator',   #this one could have interesting applications, like delayed responses to long term stimuli

    #Sensors for detecting the closest creature ()
    'genetic_distance',     #genetic closeness to the nearest creature
    'neighbor_age',
    'neighbor_color_r',
    'neighbor_color_g',
    'neighbor_color_b',
    'neighbor_defense',
    'neighbor_dir_x',
    'neighbor_dir_y',
    

]