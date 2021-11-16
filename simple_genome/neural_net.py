import numpy as np
from input_sensors import read_sensor

class NeuralNet(object):
    def __init__(self, activation_func=np.tanh, num_senses=30, num_outputs=30):
        self.connections = []
        self.neurons     = []
        #self.active_outputs = set()     #indexes of the active output neurons. It is a set to prevent repeated indexes
        self.activ_func  = activation_func

        self.num_senses  = num_senses
        self.num_outputs = num_outputs

        #-----Create the accumulators and output vectors here 
        # so that they are not created once on every feedforward computation
        #self.output_vector       = np.zeros(shape=self.num_outputs)  #this will hold the output value of the 
        #self.neuron_accumulators = np.zeros(shape=len(neurons))   #this will hold the output values of hidden neurons during feedfoward propagation
        self._container_vectors_exist = False 

    def __repr__(self):
        return f"<NeuralNet: num_connections={len(self.connections):>3} | num_hidden_neurons={self.num_hidden:>3}>"
        
    def set_up_container_vectors(self):
        self.output_vector       = np.zeros(shape=self.num_outputs)
        self.neuron_accumulators = np.zeros(shape=self.num_hidden)

        self._container_vectors_exist = True

    def set_active_outputs(self):
        self.active_outputs = []
        for conn in self.connections:
            if conn.target_type=='output':
                if conn.target_id not in self.active_outputs:
                    self.active_outputs.append(conn.target_id)

    @property 
    def num_hidden(self):
        return len(self.neurons)
    
    @property
    def num_connections(self):
        return len(self.connections)

    def feedforward(self, **sim_params):
        '''
        This function was adapted from David Miller's Github code here: https://github.com/davidrmiller/biosim4/blob/main/src/feedforward.cpp
        sim_params: dict
            Wildcard of values that can be passed to the feedforward function.
            The parameters should be simulation related parameters that would be needed to get the proper sensor readings
        '''
        if not self._container_vectors_exist:
            self.set_up_container_vectors()
            
        num_neurons = self.num_hidden
        self.output_vector.fill(0)           #reset the vector to zero
        self.neuron_accumulators.fill(0)     #reset vector to zero

        outputs_computed = False 
        for conn in self.connections:
            if conn.target_type == 'output' and (not outputs_computed):
                for neuron_idx in range(num_neurons):
                    if self.neurons[neuron_idx].driven:
                        self.neurons[neuron_idx].output = self.activ_func(self.neuron_accumulators[neuron_idx])

                outputs_computed = True 

            input_val = 0
            if conn.source_type == 'input':
                #inputVal = getSensor((Sensor)conn.sourceNum, simStep);  #check what the cpp code does with get sensor. It might be significantly different from what I need
                #input_val = 0
                #input_func = sensor_funcs.get(conn.source_id, lambda x: np.random.rand())  #if sensor does not exist for some reason, return random value [0,1]
                #sensor_func = read_sensor
                input_val = read_sensor(conn.source_id, **sim_params)
            else:
                input_val = self.neurons[conn.source_id].output
            
            if conn.target_type == 'output':
                self.output_vector[conn.target_id] += input_val * conn.weight
            else:
                self.neuron_accumulators[conn.target_id] += input_val * conn.weight

        return self.output_vector