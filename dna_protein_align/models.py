from django.db import models

# Create your models here.

class DnaSeq(models.Model):

    seq = models.TextField(help_text='Enter DNA sequence (max 1000 bp)')

    # def align(self):
    # Thinking of importing Biopython here, and then returning a dict, if that is allowed,
    # With the information to be displayed in the browser client
    # Perhaps this is not closely related to the model purpose of this class

    def __str__(self):
        # len(self.seq) may not work if TextField not coerced to str
        return 'DNA sequence: ' + str(len(self.seq)) + ' bp'
