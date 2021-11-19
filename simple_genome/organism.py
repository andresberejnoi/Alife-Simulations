from basic_types import BaseOrganism
import numpy as np

class Organism(BaseOrganism):
    POSSIBLE_MOVES = {
        0: (1,0),
        1: (1,1),
        2: (0,1),
        3: (-1,1),
        4: (-1,0),
        5: (-1,-1),
        6: (0,-1),
        7: (1,-1),
    }
    def __init__(self, x_pos=0, y_pos=0, max_x=100, max_y=100, min_x=0, min_y=0):
        super().__init__(x_pos=x_pos, y_pos=y_pos, max_x=max_x, max_y=max_y, min_x=min_x, min_y=min_y)

    def __repr__(self):
        return f"<Org: Genome_len={len(self._genome):>3} | NeuralNet Conns={self.nnet.num_connections:>3}, hidden_neurons={self.nnet.num_hidden:>3}, type={self.type.upper():>10}>"

    def think(self, **sim_params):
        '''Wrapper for nnet.feedforward to make it easier to access'''
        outputs = self.nnet.feedforward(**sim_params)
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

    def move_forward(self, movement_strength, delta_angle):
        '''This function needs to be completed. Right now it makes the 
        assumption that motion is always 1 square away'''
        
        #cur_pos = self.get_pos()
        #speed   = getattr(self, 'max_speed', 1)  #call the max speed attribute (it should exist in decoder). It is the number of cells the org can move in a single motion. Defaults to 1 if max_speed is not coded for in genome

        #motion_distance = speed * movement_strength  #the actual distance to move
        
        new_direction = self.direction + delta_angle
        
        if movement_strength==0: #org does not move, but can change angle
            self.direction = new_direction 
        
        else:
            base_pi = np.pi/4    #pi/4 will result in 8 sections of the circle around current position. It is good for when motion is only 1 square away

            discrete_square = int(new_direction / base_pi) % 8    #will result in a discrete square corresponding to an adjacent square to current position. % 8 assures we only get a value in range [0-7]
            dx, dy = self.POSSIBLE_MOVES[discrete_square]

            self.update_pos(dx, dy)
             


    