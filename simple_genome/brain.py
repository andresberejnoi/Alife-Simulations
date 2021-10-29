import numpy as np
import pprint

def make_sample_genome(input_to_hidden, input_to_ouptut, hidden_to_hidden, hidden_to_output):
    genome = []
    low = np.iinfo(np.uint16).min
    high = np.iinfo(np.uint16).max

    for pair in input_to_hidden:
        source_part = 0x00000000 | (pair[0] << 24) | np.random.randint(low, high, dtype=np.uint16)
        target_part = 0x00000000 | (pair[1] << 16) | np.random.randint(low, high, dtype=np.uint16)

        gene = source_part | target_part

        genome.append(gene)


    for pair in input_to_ouptut:
        source_part = 0x00000000 | (pair[0] << 24) | np.random.randint(low, high, dtype=np.uint16)
        target_part = 0x00800000 | (pair[1] << 16) | np.random.randint(low, high, dtype=np.uint16)

        gene = source_part | target_part

        genome.append(gene)

    for pair in hidden_to_hidden:
        source_part = 0x80000000 | (pair[0] << 24) | np.random.randint(low, high, dtype=np.uint16)
        target_part = 0x00000000 | (pair[1] << 16) | np.random.randint(low, high, dtype=np.uint16)

        gene = source_part | target_part

        genome.append(gene)

    for pair in hidden_to_output:
        source_part = 0x80000000 | (pair[0] << 24) | np.random.randint(low, high, dtype=np.uint16)
        target_part = 0x00800000 | (pair[1] << 16) | np.random.randint(low, high, dtype=np.uint16)

        gene = source_part | target_part

        genome.append(gene)

    return genome
    
    

class Connection(object):
    def __init__(self, source_type, source_id, target_type, target_id, weight) -> None:
        if isinstance(source_type, str):
            self.source_type = source_type
        else:
            self.source_type = 'input' if source_type==0 else 'hidden'
        self.source_id   = source_id

        if isinstance(target_type, str):
            self.target_type = target_type
        else:
            self.target_type = 'hidden' if target_type==0 else 'output'
        self.target_id   = target_id
        self.weight      = weight
    
    def __repr__(self):
        return f"<Conn s_type: {self.source_type:6}, s_id: {self.source_id:3} " +\
               f"| t_type: {self.target_type:6}, t_id: {self.target_id:3}| weight={self.weight:>8}>"
        
    def copy(self):
        return Connection(self.source_type, self.source_id,
                          self.target_type, self.target_id, self.weight)

class Neuron(object):
    def __init__(self, neuron_id=None, neuron_type='',):
        self.type = neuron_type
        self.id   = neuron_id
        self.output_connections = []
        self.input_connections  = []
        self._output = 0.0
        self.num_outputs = 0
        self.num_self_inputs = 0
        self.num_inputs_from_others = 0
        self.remapped_id = 0
        self.driven = True
    
    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, new_val):
        self._output = new_val

    def activate(self):
        pass

    def __repr__(self):
        return f"<Neuron type:{self.type.upper():6}, id:{self.id:>4}, remapped_id:{self.remapped_id:3}>"

class NeuralNet(object):
    def __init__(self, connections=[], neurons=[], activation_func=np.tanh, num_senses=30, num_hidden=30, num_outputs=30):
        self.connections = connections
        self.neurons     = neurons
        self.activ_func  = activation_func

        self.num_senses  = num_senses
        self.num_hidden  = num_hidden
        self.num_outputs = num_outputs

    def feedforward(self, sensory_funcs={}):
        '''
        sensory_funcs: dict
            Dictionary of callables that return a value
            for a corresponding sensor. Each key is an index
            from 0 to num_senses and the value is a function
            that takes standard parameters, as defined by the
            project description.
        '''
        num_neurons = len(self.neurons)
        output_vector       = np.zeros(shape=self.num_outputs)
        neuron_accumulators = np.zeros(shape=num_neurons)

        outputs_computed = False 
        for conn in self.connections:
            if conn.target_type == 'output' and (not outputs_computed):
                for neuron_idx in range(num_neurons):
                    if self.neurons[neuron_idx].driven:
                        self.neurons[neuron_idx].output = self.activ_func(neuron_accumulators[neuron_idx])

                outputs_computed = True 

            input_val = 0
            if conn.source_type == 'input':
                #inputVal = getSensor((Sensor)conn.sourceNum, simStep);  #check what the cpp code does with get sensor. It might be significantly different from what I need
                #input_val = 0
                input_val = sensory_funcs.get(conn.source_id, lambda: np.random.rand())  #if sensor does not exist for some reason, return random value [0,1]
            else:
                input_val = self.neurons[conn.source_id].output
            
            if conn.target_type == 'output':
                output_vector[conn.target_id] += input_val * conn.weight

        return output_vector


class BrainFactory(object):
    def __init__(self, num_senses=30, max_hidden_neurons=128, num_outputs=30, gene_length=32, section_lengths=(1,7,1,7,16)):
        self.max_hidden_neurons =  max_hidden_neurons
        self.num_senses = num_senses
        self.num_outpus = num_outputs
        
        assert(gene_length == sum(section_lengths))
        self.gene_length = gene_length

        self._set_up_masks(section_lengths)

    def _print_masks(self):
        print("* self.SOURCE_LAYER_ID_MASK:")
        print(f"{self.SOURCE_LAYER_ID_MASK:#0{self.gene_length//8}x} | {self.SOURCE_LAYER_ID_MASK:#0{self.gene_length}b}\n")

        print("* self.SOURCE_LAYER_ID_SHIFT:")
        print(f"{self.SOURCE_LAYER_ID_SHIFT:#0{self.gene_length//8}x} | {self.SOURCE_LAYER_ID_SHIFT:#0{self.gene_length}b}\n")

        print("* self.SOURCE_NEURON_ID_MASK:")
        print(f"{self.SOURCE_NEURON_ID_MASK:#0{self.gene_length//8}x} | {self.SOURCE_NEURON_ID_MASK:#0{self.gene_length}b}\n")

        print("* self.SOURCE_NEURON_ID_SHIFT:")
        print(f"{self.SOURCE_NEURON_ID_SHIFT:#0{self.gene_length//8}x} | {self.SOURCE_NEURON_ID_SHIFT:#0{self.gene_length}b}\n")

        print("* self.TARGET_LAYER_ID_MASK:")
        print(f"{self.TARGET_LAYER_ID_MASK:#0{self.gene_length//8}x} | {self.TARGET_LAYER_ID_MASK:#0{self.gene_length}b}\n")

        print("* self.TARGET_LAYER_ID_SHIFT:")
        print(f"{self.TARGET_LAYER_ID_SHIFT:#0{self.gene_length//8}x} | {self.TARGET_LAYER_ID_SHIFT:#0{self.gene_length}b}\n")

        print("* self.TARGET_NEURON_ID_MASK:")
        print(f"{self.TARGET_NEURON_ID_MASK:#0{self.gene_length//8}x} | {self.TARGET_NEURON_ID_MASK:#0{self.gene_length}b}\n")

        print("* self.TARGET_NEURON_ID_SHIFT:")
        print(f"{self.TARGET_NEURON_ID_SHIFT:#0{self.gene_length//8}x} | {self.TARGET_NEURON_ID_SHIFT:#0{self.gene_length}b}\n")

        print("* self.WEIGHT_MASK:")
        print(f"{self.WEIGHT_MASK:#0{self.gene_length//8}x} | {self.WEIGHT_MASK:#0{self.gene_length}b}\n")

        print("* self.WEIGHT_SHIFT:")
        print(f"{self.WEIGHT_SHIFT:#0{self.gene_length//8}x} | {self.WEIGHT_SHIFT:#0{self.gene_length}b}\n")

    def _set_up_masks(self, section_lengths=(1,7,1,7,16)):
        '''Creates the correct bit masks to parse a gene. By default, it is assumed
        a gene is a 32-bit unsigned number, with the following bit fields (starting from
        most significant bit):
        1 bit -> source layer ID, 7 bits -> source neuron ID, 1 bit -> target layer ID, 
        7 bits -> target neuron ID, 16 bits -> connection weight
        '''

        gene_length = self.gene_length

        masks_and_shifts_list = []

        accum_length = 0
        for length in section_lengths:
            accum_length += length
            shift = gene_length - accum_length
            mask  = int('1'*length, 2) << shift
            masks_and_shifts_list.append((mask, shift))

        _source_layer  = masks_and_shifts_list[0]
        _source_neuron = masks_and_shifts_list[1]
        _target_layer  = masks_and_shifts_list[2]
        _target_neuron = masks_and_shifts_list[3]
        _weight        = masks_and_shifts_list[4]
        
        self.SOURCE_LAYER_ID_MASK   = _source_layer[0]    #0x80000000     #1 bit
        self.SOURCE_LAYER_ID_SHIFT  = _source_layer[1]    #31

        self.SOURCE_NEURON_ID_MASK  = _source_neuron[0]   #0x7f000000     #7 bits
        self.SOURCE_NEURON_ID_SHIFT = _source_neuron[1]   #24

        self.TARGET_LAYER_ID_MASK   = _target_layer[0]    #0x00800000     #1 bit
        self.TARGET_LAYER_ID_SHIFT  = _target_layer[1]    #23

        self.TARGET_NEURON_ID_MASK  = _target_neuron[0]   #0x007f0000     #7 bits
        self.TARGET_NEURON_ID_SHIFT = _target_neuron[1]   #16

        self.WEIGHT_MASK            = _weight[0]          #0x0000ffff     #16 bits
        self.WEIGHT_SHIFT           = _weight[1]          #0

    def make_random_genome(self, num_genes):
        data_type = getattr(np, f"np.uint{self.gene_length}", np.uint32)
        low = np.iinfo(data_type).min
        high = np.iinfo(data_type).max
        return np.random.randint(low, high, size=num_genes)

    def adjust_weight(self, weight, div_factor=10_000, bit_length=16):
        data_type = getattr(np, f"int{bit_length}", np.int16)  #should be a signed 16-bit int constructor
        #low  = np.iinfo(data_type).min
        #high = np.iinfo(data_type).max 
        #byte_size = 8
        #num_bytes = bit_length // byte_size

        #bytes_weight = weight.to_bytes(num_bytes, byteorder='little')  #assumes weight is a Python int #only two bytes for a 16-bit number
        #print(weight)
        bytes_weight = weight.tobytes()   #assumes weight is a numpy int
        new_weight   = np.frombuffer(bytes_weight, dtype=data_type)[0]  #this actually returns and array so we need to get the first element
    
        return new_weight / div_factor   #the value will be around -3.2 to 3.2

    def apply_mask(self, val, mask, left_shift, astype=None):
        if astype is None:
            astype = np.uint16
        return ((val & mask) >> left_shift).astype(astype)   #assumes val is a numpy int

    def decode_gene(self, gene):
        source_type = self.apply_mask(gene, self.SOURCE_LAYER_ID_MASK, self.SOURCE_LAYER_ID_SHIFT)
        source_id   = self.apply_mask(gene, self.SOURCE_NEURON_ID_MASK, self.SOURCE_NEURON_ID_SHIFT)

        target_type = self.apply_mask(gene, self.TARGET_LAYER_ID_MASK, self.TARGET_LAYER_ID_SHIFT)
        target_id   = self.apply_mask(gene, self.TARGET_NEURON_ID_MASK, self.TARGET_NEURON_ID_SHIFT)

        weight      = self.apply_mask(gene, self.WEIGHT_MASK, self.WEIGHT_SHIFT, astype=np.int16)

        return (source_type, source_id,
                target_type, target_id,
                weight)

    def build_connection_list(self, genome):
        connection_list = []
        for gene in genome:
            source_type, source_id, target_type, target_id, weight = self.decode_gene(gene)
            weight = self.adjust_weight(weight, 10_000)    #the original code uses something closer to 8000
            #weight = weight / 10_000
            conn = Connection(source_type, source_id, target_type, target_id, weight)
            connection_list.append(conn)
        
        return connection_list

    def make_renumbered_connection_list(self, connection_list):
        renumbered_conn_list = []
        for conn in connection_list:
            renumbered_conn_list.append(conn.copy()) 
            new_conn = renumbered_conn_list[-1]
            if new_conn.source_type == 'hidden':
                new_conn.source_id %= self.max_hidden_neurons
            else:
                new_conn.source_id %= self.num_senses
            
            if new_conn.target_type == 'hidden':
                new_conn.target_id %= self.max_hidden_neurons
            else:
                new_conn.target_id %= self.num_outpus
        
        return renumbered_conn_list

    def make_node_list(self, node_dict={}, connection_list=[]):
        for conn in connection_list:
            if conn.target_type =='hidden':
                node = node_dict.get(conn.target_id, None)
                if node is None:
                    assert(conn.target_id < self.max_hidden_neurons)
                    node = Neuron(neuron_type=conn.target_type, neuron_id=conn.target_id)        #empty neuron
                    node_dict[conn.target_id] = node   
                    #node = node_dict[conn.target_id]

                    assert(conn.target_id < self.max_hidden_neurons)    #this is basically repeated from the C++ code I am trasnlating. I don't think I should keep it in Python because it seems unnecessary, but for now I am just translating
                    node.num_outputs            = 0
                    node.num_self_inputs        = 0
                    node.num_inputs_from_others = 0

                
                if conn.source_type=='hidden' and conn.source_id == conn.target_id:
                    node.num_self_inputs += 1
                else:
                    node.num_inputs_from_others += 1
                #assert(nodeMap.count(conn.sinkNum) == 1);  #c++ code. I think it needs to make sure that the map does not contain repeated keys. In python, a dictionary will take care of this automatically

            if conn.source_type == 'hidden':
                node = node_dict.get(conn.source_id, None)
                if node is None:
                    assert(conn.source_id < self.max_hidden_neurons)
                    node = Neuron(neuron_type=conn.source_type, neuron_id=conn.source_id)    #empty neuron
                    node_dict[conn.source_id] = node 

                    assert(conn.source_id < self.max_hidden_neurons)
                    node.num_outputs            = 0
                    node.num_self_inputs        = 0
                    node.num_inputs_from_others = 0

                node.num_outputs += 1
                #assert(nodeMap.count(conn.sourceNum) == 1);    #c++ code 
        return node_dict
    
    def remove_connections_to_neuron(self, connection_list=[], node_dict={}, neuron_id=1000):
        #remaining_connections = []
        #remaining_connections = [conn.copy() for conn in connection_list]
        remaining_connections = [conn for conn in connection_list]
        for conn in connection_list:
            if conn.target_type=='hidden' and conn.target_id == neuron_id:
                if conn.source_type=='hidden':
                    node_dict[conn.source_id].num_outputs -= 1
                remaining_connections.remove(conn)
            # else:   #in the original code, the else statement goes with the outer if, but because I am accumulating useful connections instead of deleting useless ones, I need to append here
            #     remaining_connections.append(conn.copy())

        return remaining_connections

    
    def cull_useless_neurons(self, node_dict={}, connection_list=[], ):
        done = False
        while not done:
            delete_keys = []
            done = True 
            for node_key in node_dict:
                assert(node_key < self.max_hidden_neurons)
                node = node_dict[node_key]

                if node.num_outputs == node.num_self_inputs:
                    done = False 
                    connection_list = self.remove_connections_to_neuron(connection_list, node_dict, node_key)
                    delete_keys.append(node_key)


            for key in delete_keys:
                del node_dict[key]    #delete useless nodes from dictionary

        return node_dict, connection_list

    def initial_neuron_output(self):   #this is a placeholder. The original C++ code calls for one function like this
        return 1.0

    def count_neuron_types(self, connection_list):
        all_inputs  = set()
        all_hidden  = set()
        all_outputs = set()
        for conn in connection_list:
            s_type = conn.source_type
            s_id   = conn.source_id 
            t_type = conn.target_type
            t_id   = conn.target_id

            if s_type == 'input':
                all_inputs.add(s_id)
            elif s_type == 'hidden':
                all_hidden.add(s_id)
            elif s_type == 'output':
                all_outputs.add(s_id)

            if t_type == 'input':
                all_inputs.add(t_id)
            elif t_type == 'hidden':
                all_hidden.add(t_id)
            elif t_type == 'output':
                all_outputs.add(t_id)
        
        num_inputs  = len(all_inputs)
        num_hidden  = len(all_hidden)
        num_outputs = len(all_outputs)

        return num_inputs, num_hidden, num_outputs

    def create_wiring_from_genome(self, genome):
        node_dict = {}

        connection_list = self.build_connection_list(genome)
        connection_list = self.make_renumbered_connection_list(connection_list)

        node_dict       = self.make_node_list(node_dict, connection_list)

        node_dict, connection_list = self.cull_useless_neurons(node_dict, connection_list)
        
        nnet = NeuralNet()

        #remap each neuron so their ids start from 0 and increase sequentially with no gaps
        assert(len(node_dict) <= self.max_hidden_neurons)
        new_number = 0
        for node_key in node_dict:
            node = node_dict[node_key]
            assert(node.num_outputs != 0)
            node.remapped_id = new_number

            new_number += 1

        #first, connections from input neurons, to hidden and hidden to hidden
        pprint.pprint(connection_list)
        nnet.connections.clear()
        for conn in connection_list:
            if conn.target_type == 'hidden':
                nnet.connections.append(conn.copy())
                new_conn = nnet.connections[-1]

                new_conn.target_id = node_dict[new_conn.target_id].remapped_id

                if new_conn.source_type == 'hidden':
                    new_conn.source_id = node_dict[new_conn.source_id].remapped_id
        
        #now we create connections to the output neurons, so that they are added at the end
        for conn in connection_list:
            if conn.target_type == 'output':
                nnet.connections.append(conn.copy())
                new_conn = nnet.connections[-1]

                if new_conn.source_type == 'hidden':
                    new_conn.source_id = node_dict[new_conn.source_id].remapped_id


        #----Calculate number of remaining neurons
        num_senses, num_hidden, num_outputs = self.count_neuron_types(connection_list)
        nnet.num_senses  = num_senses
        nnet.num_hidden  = num_hidden
        nnet.num_outputs = num_outputs
        #-----

        nnet.neurons.clear()
        for node_key in node_dict:
            node = node_dict[node_key]
            nnet.neurons.append(node)
            nnet.neurons[-1].output = self.initial_neuron_output()
            nnet.neurons[-1].driven = node_dict[node_key].num_inputs_from_others != 0  #this is a boolean

        return nnet
        
        
def test_function():
    bf = BrainFactory()
    genome = make_sample_genome(
        [(0, 10), (2,10), (1,5)],
        [(0, 2)],
        [(10, 10), (10,5),],
        [(10,2), (10, 3), (11, 10)]
    )

    nnet = bf.create_wiring_from_genome(genome)


if __name__ == '__main__':
    test_function()