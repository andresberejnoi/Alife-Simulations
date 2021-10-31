
from brain_factory import BrainFactory
from phenotype_factory import PhenotypeFactory
from genome import Genome 
from basic_types import MutationChange
import numpy as np 


class Factory(object):
    def __init__(self, gene_length     = 32, 
                 phenotype_params      = {},
                 brain_params          = {},
                 marker_genes_dict     = {},
                 point_mutation_rate   = 0.01,
                 gene_duplication_rate = 0.005,):

        self.GENE_LENGTH = gene_length  
        #self.START_BRAIN_MARKER = 0x1
        #self.END_BRAIN_MARKER   = 0x0
        self.START_BRAIN_MARKER = marker_genes_dict.get('start_brain_marker', 0x1)
        self.END_BRAIN_MARKER   = marker_genes_dict.get('end_brain_marker', 0x0)
        self.marker_genes = [self.START_BRAIN_MARKER, self.END_BRAIN_MARKER]

        self.point_mutation_rate   = point_mutation_rate
        self.gene_duplication_rate = gene_duplication_rate

        #TODO: check that brain and pheno params contain all needed info
        self.brain_factory     = BrainFactory(**brain_params)
        self.phenotype_factory = PhenotypeFactory(**phenotype_params)
        
        #----Setup functions 
        self._set_up_point_mutation_masks()
    
    def _separate_genomes(self, genome):
        '''separates full genome into phenotype genes and brain genes
        This migth not be the most efficient way, since the list will
        be traversed many more times using this method. I will check later
        if performance is an issue.
        '''
        pheno_genome = Genome(gene_length=self.GENE_LENGTH)
        brain_genome = Genome(gene_length=self.GENE_LENGTH)

        brain_mode = False 
        for gene in genome:
            if gene == self.START_BRAIN_MARKER:
                brain_mode = True 
                continue 
            elif gene == self.END_BRAIN_MARKER:
                brain_mode = False
                continue 

            if brain_mode:
                brain_genome.append(gene)
            else:
                pheno_genome.append(gene)
        return pheno_genome, brain_genome

    def create_organism(self, genome=[]):
        #first create the organism and then the brain, although
        # any order should work, I think...
        pheno_genome, brain_genome = self._separate_genomes(genome)

        org        = self.phenotype_factory.create_organism_from_genome(pheno_genome)
        org.nnet   = self.brain_factory.create_brain_from_genome(brain_genome)
        org.genome = genome
        return org

    #======================MUTATIONS========================
    def apply_point_mutations(self, genome, num_mutations=1, num_flips=1, use_genome_copy=False, protect_guards=True):
        '''Randomly applies a mutation masks to a random gene or genes
        protect_guards: bool
            If True, a mutation will not be applied to marker genes,
            such as self.START_BRAIN_MARKER and self.END_BRAIN_MARKER'''
        data_type = getattr(np, f"uint{self.GENE_LENGTH}", np.uint32)

        if use_genome_copy:
            genome = Genome([gene for gene in genome])    #this local variable will reference a copy of the passed list

        if num_flips=='random':
            num_flips = np.random.randint(0, self.GENE_LENGTH, dtype=data_type)
        elif isinstance(num_flips, list):
            lower_bound = num_flips[0]
            upper_bound = num_flips[1]
            num_flips = np.random.randint(lower_bound,upper_bound, dtype=data_type)
        
        len_genome = len(genome)
        changes = []
        for i in range(num_mutations):
            rnd_gene_idx = np.random.randint(0, len_genome, dtype=data_type)
            mutation_mask = self._get_composite_mutation_mask(num_flips, data_type)

            _change = MutationChange(gene_idx=rnd_gene_idx, original_gene=genome[rnd_gene_idx])
            if protect_guards:
                while genome[rnd_gene_idx] in self.marker_genes:
                    rnd_gene_idx = np.random.randint(0, len_genome, dtype=data_type)   #keep getting a new idx until it is not a marker gene
            genome[rnd_gene_idx] ^= mutation_mask   #this flips the bit or bits

            _change.mutation_mask = mutation_mask
            _change.changed_gene  = genome[rnd_gene_idx]
            changes.append(_change)
        return genome, changes

    def _get_composite_mutation_mask(self,num_flips=1, data_type=np.uint32):
        '''Create a mutation mask that can have 1 or more genes flipped.'''
        mutation_mask = 0
        for i in range(num_flips):
            random_shift = np.random.randint(0, self.GENE_LENGTH, dtype=data_type)
            bit_to_flip = self._point_mutation_masks[random_shift]
            mutation_mask = mutation_mask | bit_to_flip
        return mutation_mask

    def _set_up_point_mutation_masks(self):
        self._point_mutation_masks = []
        shifting_mask = 0x1
        for i in range(self.GENE_LENGTH):
            self._point_mutation_masks.append(shifting_mask << i)

    def apply_gene_duplication_error(self):
        pass
