import yaml
import numpy as np
from genome import Genome

def get_settings_from_file(filename=''):
    default_file = 'default_config.yml'
    try:
        #filename = "default_config.yml"
        f_handler = open(filename)
    except (FileNotFoundError, TypeError) as e:
        f_handler = open(default_file)
        print(f"* Error:\n{e}\n\t* Could not open provided filename: {filename}.\n\t-> Opening default file instead: {default_file}")
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

    return list(pheno_genes) + list(brain_genes)

def show_org_info(org):
    print(f"\n{'-'*80}")
    new_line = '\n\t'
    print(f"\n* Neural net:\n{org.nnet}") 
    print(f"\n* Neurons:\n\t{new_line.join([str(neuron) for neuron in org.nnet.neurons])}")
    print(f"\n* Connections:\n\t{new_line.join([str(conn) for conn in org.nnet.connections])}") 
    print(f"\n* Neuron Accumulator:\n\t{org.nnet.neuron_accumulators}" )
    #f"\n* Org Genome:\n\t{new_line.join([bin(gene) for gene in org.genome])}" )
    
    print("\nGenome:\n")
    print("\t" + "\n\t".join([f"{gene:032b}" for gene in org.genome]))

