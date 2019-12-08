from Bio.Alphabet import generic_dna
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment

class Aligner():

    PROTEIN_NAMES = ['NC_000852', 'NC_007346', 'NC_008724', 'NC_009899', 'NC_014637', 'NC_020104', 'NC_023423', 'NC_023640',
                'NC_023719', 'NC_027867']
    proteins = None

    # If they're small enough, you can just deploy them as static files - I'll assume that for now

    '''    def load_proteins(self):
        for protein in PROTEINS
    '''

    def find_seq(self, input_seq_string):
        for protein_name in self.PROTEIN_NAMES:
            # This can be made more efficient by avoiding f.read() (except you're going to read the
            # whole thing anyway in a search, but here you are reading it twice, in read() and find()
            with open('dna_protein_align/resources/' + protein_name + '.txt', 'r') as f:
            #import io
            #with io.StringIO('AAGGCCC') as f:
                trans_protein_seq = f.read()
                index = trans_protein_seq.find(input_seq_string)
                if index != -1:
                    return protein_name, index
        return None