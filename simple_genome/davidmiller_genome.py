"""
This file is intended as a rough translation of David Miller's C++ code
on Github. The original file `genome.cpp` is found at this link:
https://github.com/davidrmiller/biosim4/blob/main/src/genome.cpp

I made minor modifications to fit with the way Python works and added
a couple of helpful functions. This file can help make the code more accessible.

Additionally, I changed a few of the variable names used in the original code
to better fit with the way I understand the problem. For example, in the C++
code, `NEURON` refers to the hidden neurons in my code, while sensors and actions 
refer to what I call input and output neurons, respectively.
"""

SOURCE_LAYER_ID_MASK    = 0x80000000    #1 bit
SOURCE_LAYER_ID_SHIFT   = 31

SOURCE_NEURON_ID_MASK   = 0x7f000000    #7 bits
SOURCE_NEURON_ID_SHIFT  = 24

TARGET_LAYER_ID_MASK   = 0x00800000     #1 bit
TARGET_LAYER_ID_SHIFT  = 23

TARGET_NEURON_ID_MASK  = 0x007f0000     #7 bits
TARGET_NEURON_ID_SHIFT = 16

WEIGHT_MASK            = 0x0000ffff     #16 bits
WEIGHT_SHIFT           = 0

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
        return f"<Conn s_type: {self.source_type}, s_id: {self.source_id} " +\
               f"| t_type: {self.target_type}, t_id: {self.target_id} | weight={self.weight}>"
        
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
        return f"<Neuron type:{self.type.upper()}, id:{self.id}, remapped_id:{self.remapped_id}>"

class NeuralNet(object):
    def __init__(self, connections=[], neurons=[]):
        self.connections = connections
        self.neurons     = neurons

#----------------------------------
def adjust_weight(weight, div_factor=10_000, bit_length=16):
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

def apply_mask(val, mask, left_shift, astype=None):
    if astype is None:
        astype = np.uint16
    return ((val & mask) >> left_shift).astype(astype)   #assumes val is a numpy int

def decode_gene(gene):
    source_type = apply_mask(gene, SOURCE_LAYER_ID_MASK, SOURCE_LAYER_ID_SHIFT)
    source_id   = apply_mask(gene, SOURCE_NEURON_ID_MASK, SOURCE_NEURON_ID_SHIFT)

    target_type = apply_mask(gene, TARGET_LAYER_ID_MASK, TARGET_LAYER_ID_SHIFT)
    target_id   = apply_mask(gene, TARGET_NEURON_ID_MASK, TARGET_NEURON_ID_SHIFT)

    weight      = apply_mask(gene, WEIGHT_MASK, WEIGHT_SHIFT, astype=np.int16)

    return (source_type, source_id,
            target_type, target_id,
            weight)

def build_connection_list(genome):
    connection_list = []
    for gene in genome:
        source_type, source_id, target_type, target_id, weight = decode_gene(gene)
        weight = adjust_weight(weight, 10_000)    #the original code uses something closer to 8000
        #weight = weight / 10_000
        conn = Connection(source_type, source_id, target_type, target_id, weight)
        connection_list.append(conn)
    
    return connection_list

max_number_hidden_neurons = 40
num_senses  = 20
num_outputs = 10


def initial_neuron_output():   #this is a placeholder. The original C++ code calls for one function like this
    return 1.0
#============================================================
# Here is where the actual translation from genome.cpp starts
# I just translated the main functions that deal with setting 
# up the neural network, such as renumbering the connections 
# and neurons and removing unused nodes. Some things have changed
# from the original code to match what I thought was the intent, 
# but I'm not proficient in C++, so I probably made some mistakes.
# However, I tested the code and it worked, at least on my limited tests

def make_renumbered_connection_list(connection_list, renumbered_conn_list=[]):
    renumbered_conn_list = []
    for conn in connection_list:
        renumbered_conn_list.append(conn.copy()) 
        new_conn = renumbered_conn_list[-1]
        if new_conn.source_type == 'hidden':
            new_conn.source_id %= max_number_hidden_neurons
        else:
            new_conn.source_id %= num_senses
        
        if new_conn.target_type == 'hidden':
            new_conn.target_id %= max_number_hidden_neurons
        else:
            new_conn.target_id %= num_outputs
    
    return renumbered_conn_list

def make_node_list(node_dict={}, connection_list=[]):
    for conn in connection_list:
        if conn.target_type =='hidden':
            node = node_dict.get(conn.target_id, None)
            if node is None:
                assert(conn.target_id < max_number_hidden_neurons)
                node = Neuron(neuron_type=conn.target_type, neuron_id=conn.target_id)        #empty neuron
                node_dict[conn.target_id] = node   
                #node = node_dict[conn.target_id]

                assert(conn.target_id < max_number_hidden_neurons)    #this is basically repeated from the C++ code I am trasnlating. I don't think I should keep it in Python because it seems unnecessary, but for now I am just translating
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
                assert(conn.source_id < max_number_hidden_neurons)
                node = Neuron(neuron_type=conn.source_type, neuron_id=conn.source_id)    #empty neuron
                node_dict[conn.source_id] = node 

                assert(conn.source_id < max_number_hidden_neurons)
                node.num_outputs             = 0
                node.num_self_inputs        = 0
                node.num_inputs_from_others = 0

            node.num_outputs += 1
            #assert(nodeMap.count(conn.sourceNum) == 1);    #c++ code 
    return node_dict

def remove_connections_to_neuron(connection_list, node_dict, neuron_id):
    remaining_connections = [conn for conn in connection_list]
    for conn in connection_list:
        if conn.target_type=='hidden' and conn.target_id == neuron_id:
            if conn.source_type=='hidden':
                node_dict[conn.source_id].num_outputs -= 1
            remaining_connections.remove(conn)
        # else:   #in the original code, the else statement goes with the outer if, but because I am accumulating useful connections instead of deleting useless ones, I need to append here
        #     remaining_connections.append(conn.copy())

    return remaining_connections

def cull_useless_neurons(connection_list, node_dict):
    done = False

    
    while not done:
        delete_keys = []
        done = True 
        for node_key in node_dict:
            assert(node_key < max_number_hidden_neurons)
            node = node_dict[node_key]

            if node.num_outputs == node.num_self_inputs:
                done = False 
                connection_list = remove_connections_to_neuron(connection_list, node_dict, node_key)
                delete_keys.append(node_key)


        for key in delete_keys:
            del node_dict[key]    #delete useless nodes from dictionary

    return node_dict, connection_list

def create_wiring_from_genome(connection_list):
    node_dict = {}
    #connection_list = []

    connection_list = make_renumbered_connection_list(connection_list)
    #print(f"\n* AFTER make_renumbered_connection_list (len={len(connection_list)}):\n")
    #pprint.pprint(connection_list)

    node_dict       = make_node_list(node_dict, connection_list)
    # print(f"\n* AFTER make_node_list (len={len(node_dict)}):\n")
    # pprint.pprint(node_dict)

    node_dict, connection_list = cull_useless_neurons(connection_list, node_dict)
    # print(f"\n* AFTER cull_useless_neurons (len={len(node_dict)}):\n")
    # pprint.pprint(node_dict)

    nnet = NeuralNet()
    #return nnet

    #remap each neuron so their ids start from 0 and increase sequentially with no gaps
    assert(len(node_dict) <= max_number_hidden_neurons)
    #remapped_node_dict = {}
    new_number = 0
    for node_key in node_dict:
        node = node_dict[node_key]
        assert(node.num_outputs != 0)
        node.remapped_id = new_number

        #remapped_node_dict[node.remapped_id] = node
        new_number += 1
    
    # print(f"\n* BEFORE remapping neurons (len={len(node_dict)}):\n")
    # pprint.pprint(node_dict)
    # #node_dict = remapped_node_dict
    # print(f"\n* AFTER remapping neurons (len={len(node_dict)}):\n")
    # pprint.pprint(node_dict)

    # print(f"\n* CONNECTIONS After remapping neurons (len={len(connection_list)}):\n")
    # pprint.pprint(connection_list)
    
    

    #first, connections from input neurons, to hidden and hidden to hidden
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

    # print(f"\n* nnet.connections after adding connections (len={len(nnet.connections)}):\n")
    # pprint.pprint(nnet.connections)

    nnet.neurons.clear()
    #pprint.pprint(node_dict)
    #for neuron_id in range(len(node_dict)):   #this line does not work here. I don't know if I missed something, but following the C++ code as is, the key values from nodeMap never get updated, so this always ends up raising a key error this way
    for node_key in node_dict:
        node = node_dict[node_key]
        nnet.neurons.append(node)
        #print(nnet.neurons)
        nnet.neurons[-1].output = initial_neuron_output()
        nnet.neurons[-1].driven = node_dict[node_key].num_inputs_from_others != 0  #this is a boolean
    
    # print(f"\n* nnet.neurons after adding connections (len={len(nnet.neurons)}):\n")
    # pprint.pprint(nnet.neurons)

    return nnet

if __name__ == '__main__':
    import numpy as np
    import pprint 

    data_type       = np.uint32    #unsigned 32-bit int
    low             = np.iinfo(data_type).min
    high            = np.iinfo(data_type).max 
    num_connections = 25

    #----Making Genome   (use numpy since some internal parts assume numpy types)
    genome    = np.random.randint(low, high, size=num_connections, dtype=data_type)

    #----Build Initial Connection List
    connection_list = build_connection_list(genome)

    #----Create the Neural Network
    nnet = create_wiring_from_genome(connection_list)

    #----Show the inside of the network
    print(f"\n* Neural Net Connections (len={len(nnet.connections)}):\n")
    pprint.pprint(nnet.connections)

    print(f"\n* Neural Net Neurons (len={len(nnet.neurons)}):\n")
    pprint.pprint(nnet.neurons)