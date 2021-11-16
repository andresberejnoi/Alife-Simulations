import yaml
import numpy as np

def get_settings_from_file(filename=''):
    default_file = 'default_config.yml'
    try:
        #filename = "default_config.yml"
        f_handler = open(filename)
    except (FileNotFoundError, TypeError) as e:
        f_handler = open(default_file)
        print(f"-> Could not open provided filename: {filename}. Opening default file instead: {default_file}")
    config = yaml.safe_load(f_handler)
    f_handler.close()
    return config

def make_random_genome(num_genes, 
                       num_brain_connections,
                       gene_length=32,
                       start_brain_marker=0x1,
                       end_brain_marker=0x0,
                       rng=None):
    
    data_type   = getattr(np, f"uint{gene_length}", np.uint32)
    low         = np.iinfo(data_type).min
    high        = np.iinfo(data_type).max

    if rng is None:
        rng = np.random.default_rng()
    
    #pheno_genes = np.random.randint(low, high, size=num_genes, dtype=data_type) 
    #brain_genes = np.random.randint(low, high, size=num_brain_connections+2, dtype=data_type)  #+2 to account for marker genes 
    pheno_genes = rng.integers(low, high, size=num_genes, dtype=data_type)
    brain_genes = rng.integers(low, high, size=num_brain_connections+2, dtype=data_type)    #+2 to account for marker genes 

    brain_genes[0]  = start_brain_marker
    brain_genes[-1] = end_brain_marker

    return list(pheno_genes) + list(brain_genes)

def get_distance(p1=(0,0), p2=(0,0)):
    '''get discrete distance'''
    x1, y1 = p1
    x2, y2 = p2 

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return max([dx,dy])

def show_org_info(org):
    print(f"\n{'-'*80}")
    print(f"Organism Details are:\n{org}")
    new_line = '\n\t'
    print(f"\n* Neural net:\n{org.nnet}") 
    print(f"\n* Neurons ({len(org.nnet.neurons)}):\n\t{new_line.join([str(neuron) for neuron in org.nnet.neurons])}")
    print(f"\n* Connections ({len(org.nnet.connections)}):\n\t{new_line.join([str(conn) for conn in org.nnet.connections])}") 
    print(f"\n* Neuron Accumulators:\n\t{org.nnet.neuron_accumulators}" )
    print(f"\n* Neuron Output Vector:\n\t{org.nnet.output_vector}")
    #f"\n* Org Genome:\n\t{new_line.join([bin(gene) for gene in org.genome])}" )
    
    print("\nGenome (Readable):\n")
    print("\t" + "\n\t".join([f"{gene:032b}" for gene in org.genome]))

    print("\nGenome (list form):")
    print(f"{org.genome}")



def show_two_orgs(org1, org2):
    '''A monster of a function. Provide to Organism objects and it will print their information side by side.
    This is mostly for debugging. The function looks very ugly as it is, but it works.'''
    side_len = 80
    new_line = '\n'
    sep      = "||"
    offset   = 2 + len(sep)
    #---print each org side by side:
    print(f"{'Org1':^{side_len}} {sep} {'Org2':^{side_len}}")
    print(f"{'='*((side_len*2) + offset)}")
    print(f"\nOrganism Details are:\n{str(org1):>{side_len}} {sep} {str(org2):<{side_len}}")

    print(f"\n{'-'*((side_len*2) + offset)}")
    print(f"\nNeural Nets:\n{str(org1.nnet):>{side_len}} {sep} {str(org2.nnet):<{side_len}}")

    #==============================================
    #---Printing Neurons
    print(f"\n{'-'*((side_len*2) + offset)}")
    print(f"\n{'Neurons (' + str(len(org1.nnet.neurons)) + ')':^{side_len}} {sep} ", end='')  #using end to connect this print to the next in one line
    print(f"{'Neurons (' + str(len(org2.nnet.neurons)) + ')' + new_line:^{side_len}}")


    #---Printing Neurons
    neuron_lines = []
    empty_line = f"{'~'*25:^{side_len}}"
    for i in range(len(org1.nnet.neurons)):
        org1_neuron = org1.nnet.neurons[i]
        line = f"{str(org1_neuron):>{side_len}}"
        pair = [line, empty_line]
        neuron_lines.append(pair)

    for i in range(len(org2.nnet.neurons)):
        org2_neuron = org2.nnet.neurons[i]
        line = f"{str(org2_neuron):<{side_len}}"

        try:
            pair = neuron_lines[i]
            pair[1] = line
        except IndexError:
            pair = [empty_line, line]
            neuron_lines.append(pair)

    list_lines = []
    for line in neuron_lines:
        str_line = " || ".join(line)
        list_lines.append(str_line)
    
    str_lines = "\n".join(list_lines)
    print(f"{str_lines}")

    #==============================================
    #------------Priting Connections
    print(f"\n{'-'*((side_len*2) + offset)}")
    print(f"\n{'Connections (' + str(len(org1.nnet.connections)) + ')':^{side_len}} {sep} ", end='')
    print(f"{'Connections (' + str(len(org2.nnet.connections)) + ')' + new_line:^{side_len}}\n")


    conn_lines = []
    for i in range(len(org1.nnet.connections)):
        conn = org1.nnet.connections[i]
        line = f"{str(conn):>{side_len}}"
        pair = [line, empty_line]
        conn_lines.append(pair)

    for i in range(len(org2.nnet.connections)):
        conn = org2.nnet.connections[i]
        line = f"{str(conn):<{side_len}}"

        try:
            pair = conn_lines[i]
            pair[1] = line
        except IndexError:
            pair = [empty_line, line]
            conn_lines.append(pair)
    
    list_lines = []
    for line in conn_lines:
        str_line = " || ".join(line)
        list_lines.append(str_line)
    
    str_lines = "\n".join(list_lines)
    print(f"{str_lines}")



    #=========================================
    #----------------Printing Neuron Accumulators
    print(f"\n{'-'*((side_len*2) + offset)}")
    print(f"\n{'Neuron Accumulators (' + str(len(org1.nnet.neuron_accumulators)) + ')':^{side_len}} {sep} ", end='')
    print(f"{'Neuron Accumulators (' + str(len(org2.nnet.neuron_accumulators)) + ')' + new_line:^{side_len}}\n")

    print(f"{str(org1.nnet.neuron_accumulators):>{side_len}} {sep} {str(org2.nnet.neuron_accumulators):<{side_len}}")

    #==========================================
    #---------------Printing Genome (readable)
    print(f"\n{'-'*((side_len*2) + offset)}")
    print(f"\n{'Genome (readable) (' + str(len(org1.genome)) + ')':^{side_len}} {sep} ", end='')
    print(f"{'Genome (readable) (' + str(len(org2.genome)) + ')' + new_line:^{side_len}}\n")

    genome_lines = []
    for i in range(len(org1.genome)):
        gene = org1.genome[i]
        _line = f"{gene:>032b}"
        line = f"{_line:>{side_len}}"
        pair = [line, empty_line]
        genome_lines.append(pair)

    for i in range(len(org2.genome)):
        gene = org2.genome[i]
        _line = f"{gene:<032b}"
        line = f"{_line:<{side_len}}"

        try:
            pair = genome_lines[i]
            pair[1] = line
        except IndexError:
            pair = [empty_line, line]
            genome_lines.append(pair)

    list_lines = []
    for line in genome_lines:
        str_line = " || ".join(line)
        list_lines.append(str_line)
    
    str_lines = "\n".join(list_lines)
    print(f"{str_lines}")


    #================================================================
    #--------------------Printing genome in list form
    print(f"\n{'-'*((side_len*2) + offset)}")
    print("\nGenomes in Printable Format:")
    print(f"\n{'Genome Org1 (list form) (' + str(len(org1.genome)) + '):'}")
    print(f"\n{org1.genome}")

    print(f"\n{'Genome Org2 (list form) (' + str(len(org2.genome)) + '):'}")
    print(f"\n{org2.genome}")

#TODO: this function below needs polishing. It was copied directly from a Jupyter notebook with no changes
#TODO: right now the function can swap the position of org1 and org2 depending on which one is longer. I would prefer it to maintain positions
def print_two_orgs_attributes(org1, org2):
    ""
    atts1 = {at:i for i,at in enumerate(dir(org1))}
    atts2 = {at:i for i,at in enumerate(dir(org2))}

    top_len = len(atts1) if len(atts1) >= len(atts2) else len(atts2)
    longest  = atts1 if len(atts1) >= len(atts2) else atts2
    shortest = atts2 if len(atts2) > len(atts1) else atts1

    side_len = 25
    print(f"{'Atts Org1':^{side_len}} | {'Atts Org2':^{side_len}}\n{'-'*((side_len*2)+3)}")
    for key in longest:
        if key.startswith('_'):
            continue
        s_key = key if key in shortest else None
        print(f"{key:^{side_len}} | {s_key:^{side_len}}")