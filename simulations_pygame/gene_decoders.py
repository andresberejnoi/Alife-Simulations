def eye_decoder(self, gene, *params):
    props = gene.properties
    val   = gene.value

    #assuming gene is a 32-bit int
    rgb_mask  = 0x00380000
    rgb_shift = 19

    rgb_vals = (gene & rgb_mask) >> rgb_shift
    has_r = (rgb_vals & 0x4) >> 2
    has_g = (rgb_vals & 0x2) >> 1
    has_b = (rgb_vals & 0x1)