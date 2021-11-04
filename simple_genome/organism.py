from basic_types import BaseOrganism


class Organism(BaseOrganism):
    def __init__(self, x_pos=0, y_pos=0, max_x=100, max_y=100, min_x=0, min_y=0):
        super().__init__(x_pos=x_pos, y_pos=y_pos, max_x=max_x, max_y=max_y, min_x=min_x, min_y=min_y)

    def __repr__(self):
        return f"<Org: Genome_len={len(self._genome):>3} | NeuralNet Conns={self.nnet.num_connections:>3}, hidden_neurons={self.nnet.num_hidden:>3}, type={self.type.upper():>10}>"

    def think(self, sensor_funcs={}):
        '''Wrapper for nnet.feedforward to make it easier to access'''
        outputs = self.nnet.feedforward(sensor_funcs)
        return outputs

    def move(self, dx, dy):
        """
        dx: int
            Change in the x direction (width) with respect to current position.
        dy: int
            Change in the y direction (height) with respect to current position.
        """
        self.x_pos += dx 
        self.y_pos += dy

        return self.y_pos, self.x_pos