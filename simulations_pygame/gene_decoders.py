from types import SimpleNamespace

def eye_decoder(self, gene, *params):
    pass 


class DefaultGeneDecoder(object):
    def __init__(self, name, gene_id, gene_body):
        self.name      = name
        self.gene_id   = gene_id
        self.gene_body = gene_body

    def __repr__(self) -> str:
        return f"<Gene decoder for: {self.name.upper()} (id: {self.gene_id})>"

    @classmethod
    def make_bool(cls, str_bit):
        assert (len(str_bit) == 1)
        return bool(int(str_bit))

class EyeDecoder(DefaultGeneDecoder):
    def decode(self):
        str_bits = f"{self.gene_body:b}"    #returns the binary representation of the number, excluding the '0b' at the beginning
        
        rgb_ultraviolet = (self.make_bool(str_bits[0]),
                           self.make_bool(str_bits[1]),
                           self.make_bool(str_bits[2]),
                           self.make_bool(str_bits[3]))


        eye_attributes = SimpleNamespace(
            red   = (True if str_bits[0]=='1' else False),
            green = (True if str_bits[1]=='1' else False),
            blue  = (True if str_bits[2]=='1' else False),
            uv    = (True if str_bits[3]=='1' else False),
            #rgb   = (int(red), int(green), int(blue))
        )

def decode_metabolic_gene(gene_switch, gene_id, gene_body):
    str_bits = f"{gene_body}"

