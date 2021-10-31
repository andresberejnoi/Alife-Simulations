import yaml
import numpy as np
from genome import Genome

def get_settings_from_file(filename=''):

    try:
        #filename = "default_config.yml"
        f_handler = open(filename)
    except FileNotFoundError:
        f_handler = open('default_config.yml')

    config = yaml.safe_load(f_handler)
    f_handler.close()
    return config

def make_random_genome(num_genes, 
                       num_brain_connections,
                       gene_length=32,
                       start_brain_marker=0x1,
                       end_brain_marker=0x0):
    
    data_type   = getattr(np, f"uint{gene_length}", np.uint32)
    low         = np.iinfo(data_type).min
    high        = np.iinfo(data_type).max
    
    pheno_genes = np.random.randint(low, high, size=num_genes, dtype=data_type) 
    brain_genes = np.random.randint(low, high, size=num_brain_connections+2, dtype=data_type)  #+2 to account for marker genes 
    
    brain_genes[0]  = start_brain_marker
    brain_genes[-1] = end_brain_marker

    return Genome(list(pheno_genes) + list(brain_genes), gene_length=gene_length)