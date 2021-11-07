import numpy as np

class NeuralNet(object):
    def __init__(self, connections=[], neurons=[], activation_func=np.tanh, num_senses=30, num_outputs=30):
        self.connections = connections
        self.neurons     = neurons
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
        self.output_vector = np.zeros(shape=self.num_outputs)
        self.neuron_accumulators = np.zeros(shape=self.num_hidden)
        self._container_vectors_exist = True

    @property 
    def num_hidden(self):
        return len(self.neurons)
    
    @property
    def num_connections(self):
        return len(self.connections)

    def feedforward(self, sensor_funcs={}):
        '''
        sensory_funcs: dict
            Dictionary of callables that return a value
            for a corresponding sensor. Each key is an index
            from 0 to num_senses and the value is a function
            that takes standard parameters, as defined by the
            project description.
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
                input_func = sensor_funcs.get(conn.source_id, lambda x: np.random.rand())  #if sensor does not exist for some reason, return random value [0,1]
                input_val = input_func(self)
            else:
                input_val = self.neurons[conn.source_id].output
            
            if conn.target_type == 'output':
                self.output_vector[conn.target_id] += input_val * conn.weight
            else:
                self.neuron_accumulators[conn.target_id] += input_val * conn.weight

        return self.output_vector