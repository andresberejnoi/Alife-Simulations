from basic_types import BaseOrganism


class Organism(BaseOrganism):
    def __init__(self, init_xy=(0,0), max_xy=(500,500), min_xy=(-500,-500), genome=[]):
        super().__init__(init_xy=init_xy, max_xy=max_xy, min_xy=min_xy, genome=genome)

    def __repr__(self):
        return f"<Org: Genome_len={len(self._genome):>3} | NeuralNet Conns={self.nnet.num_connections:>3}, hidden_neurons={self.nnet.num_hidden:>3}>"

    def think(self):
        outputs = self.nnet.feedforward(sensor_funcs={})
        return outputs