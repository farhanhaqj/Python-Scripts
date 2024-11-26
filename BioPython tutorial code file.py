#!/usr/bin/env python
# coding: utf-8

# In[6]:


from Bio import pairwise2
from Bio.pairwise2 import format_alignment

def pairwise_alignment(seq1, seq2, alignment_type = 'global'):
    if alignment_type == 'global':
        alignments = pairwise2.align.globalxx(seq1, seq2)
        
    elif alignment_type == 'local':
        alignments = pairwise2.align.localxx(seq1, seq2)
    
    else:
        raise ValueError('Invalid alignment type!')
      
    for i in alignments:
        print(format_alignment(*i))
        
    return 

dna_seq1 = 'ATCTGCCGTA'
dna_seq2 = 'ATGTGCTGAA'

pairwise_alignment(dna_seq1, dna_seq2)

    
        
    



# In[ ]:




