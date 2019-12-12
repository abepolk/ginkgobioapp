from random import shuffle

class Aligner():

    # Proteins stored as static files in directory dna_protein_align/resources

    protein_names = ['NC_000852', 'NC_007346', 'NC_008724', 'NC_009899', 'NC_014637', 'NC_020104', 'NC_023423',
                        'NC_023640', 'NC_023719', 'NC_027867']


    def find_seq(self, input_seq_string):
        # Proteins must be searched in random order, so shuffle is used
        shuffle(self.protein_names)
        for protein_name in self.protein_names:
            # This can be made more efficient by avoiding f.read() combined with string.find()
            with open('dna_protein_align/resources/' + protein_name + '.txt', 'r') as f:
                trans_protein_seq = f.read()
                # Want base pairs to be 1-indexed, not 0-indexed as in Python, so add 1
                index = trans_protein_seq.find(input_seq_string) + 1
                # Find returns minus one if sequence not found, and -1 + 1 = 0, and line above has + 1
                if index != 0:
                    return protein_name, index
        return None