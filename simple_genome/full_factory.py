
from brain_factory import BrainFactory
from phenotype_factory import PhenotypeFactory
from genome import Genome 
from basic_types import MutationChange
from tools import get_settings_from_file
import numpy as np 


def make_factory_from_config(config_filename=None, decoders={}):
    config = get_settings_from_file(config_filename)

    num_genes       = config['simulation']['num_pheno_genes']
    num_brain_conns = config['simulation']['num_brain_conns']
    num_senses      = 20
    num_outputs     = 20

    gene_length           = config['phenotype_genome']['gene_length']
    mutation_rate         = config['mutation']['point_mutation_rate']
    gene_duplication_rate = config['mutation']['gene_duplication_rate']
    marker_genes_dict     = config['marker_genes']

    brain_params = config['brain_genome']
    brain_params['num_outputs'] = num_outputs
    brain_params['num_senses']  = num_senses

    pheno_params = config['phenotype_genome']
    pheno_params['gene_decoders'] = decoders

    factory = Factory(gene_length       = gene_length,
                  phenotype_params      = pheno_params,
                  brain_params          = brain_params,
                  marker_genes_dict     = marker_genes_dict,
                  num_pheno_genes       = num_genes,
                  num_brain_conns       = num_brain_conns,
                  point_mutation_rate   = mutation_rate,
                  gene_duplication_rate = gene_duplication_rate,)
    return factory

class Factory(object):
    def __init__(self, gene_length     = 32, 
                 phenotype_params      = {},
                 brain_params          = {},
                 marker_genes_dict     = {},
                 num_pheno_genes       = 10,
                 num_brain_conns       = 15,
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
        pheno_genome = []    #Genome(gene_length=self.GENE_LENGTH)
        brain_genome = []    #Genome(gene_length=self.GENE_LENGTH)

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
        org.nnet   = self.brain_factory.create_brain_from_genome(brain_genome,)
        org.genome = [gene for gene in genome]    #TODO: I think I need this to make sure each organism has its own genome and not a reference to someone else's
        return org

    #======================MUTATIONS========================
    def apply_point_mutations(self, 
                              genome, 
                              num_mutations=1, 
                              num_flips=1, 
                              use_genome_copy=False, 
                              protect_guards=True,
                              prevent_repeated_mutations=True):
        '''Randomly applies a mutation masks to a random gene or genes (each mutation mask
        will be randomly generated for each gene to mutate).

        PARAMETERS
        ----------
        num_mutations: int
            Number of genes from genome to mutate. The mutation will be applied to a 
            random location in the genome. 
        num_flips: int, str, list, tuple:
            Number of bits to flip in a single gene. If int, then the number 
            to flip is fixed. If str, then the only valid value is 'random'
            and it will result in a mask where anywhere from 0 to self.GENE_LENGTH
            bits will be flipped. 
            If tuple or list, it should contain at least two elements. The first element
            is the lower bound for a random number and the second element is the upper 
            bound. This will also result in a random number of flips, but this allows to
            control the min and max of the possible flips.
        protect_guards: bool
            If True, a mutation will not be applied to marker genes,
            such as self.START_BRAIN_MARKER and self.END_BRAIN_MARKER
        prevent_repeated_mutations: bool
            If True, the function will keep track of which gene positions have been modified
            already and prevent the same ones from being selected for the next mutation. 
            This parameter is only useful if num_mutations > 1.
        
        RETURNS
        -------
        genome: Genome, list
            A Genome object, or list containing the mutations that were applied.
        changes: list
            List of MutationChange objects to keep track of all changes applied to the genome'''

        data_type = getattr(np, f"uint{self.GENE_LENGTH}", np.uint32)

        if use_genome_copy:
            genome = Genome([gene for gene in genome])    #this local variable will reference a copy of the passed list

        if num_flips=='random':
            num_flips = np.random.randint(0, self.GENE_LENGTH, dtype=data_type)  #number of bits to flip in a single gene will be from 0 to self.GENE_LENGTH-1, selected randomly
        elif isinstance(num_flips, list) or isinstance(num_flips, tuple):
            lower_bound = num_flips[0]
            upper_bound = num_flips[1]
            num_flips = np.random.randint(lower_bound,upper_bound, dtype=data_type)
        
        len_genome = len(genome)
        changes = []            #keep track of the changes applied
        if prevent_repeated_mutations and num_mutations > 1:
            allowed_genome_positions = list(range(len(genome)))
        else:
            allowed_genome_positions = []

        for i in range(num_mutations):

            if prevent_repeated_mutations:
                _helper_idx = np.random.randint(0, len(allowed_genome_positions), dtype=data_type)
                rnd_gene_idx = allowed_genome_positions.pop(_helper_idx)    #remove the idx that has already been used
            else:
                rnd_gene_idx = np.random.randint(0, len_genome, dtype=data_type)

            if protect_guards:
                while genome[rnd_gene_idx] in self.marker_genes:
                    rnd_gene_idx = np.random.randint(0, len_genome, dtype=data_type)   #keep getting a new idx until it is not a marker gene
            
            original_gene = genome[rnd_gene_idx]

            mutation_mask = self._get_composite_mutation_mask(num_flips, data_type)
            genome[rnd_gene_idx] ^= mutation_mask   #this flips the bit or bits

            _change = MutationChange(gene_idx=rnd_gene_idx,
                                     original_gene=original_gene,
                                     mutation_mask=mutation_mask,
                                     changed_gene=genome[rnd_gene_idx])
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
