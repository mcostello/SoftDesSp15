# -*- coding: utf-8 -*-
"""
Created on Sun Jan  20 11:24:42 2015

@author: Michael Costello

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

def get_complement(nucleotide):

    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """

    nucDict={'A':'T','G':'C','T':'A','C':'G'}
    return(nucDict[nucleotide])


def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specified DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    n = len(dna)
    reverse_dna = []

    for i in range(n):
        reverse_dna.append (get_complement(dna[n - 1 - i]))
    reverse_complement = ''.join(reverse_dna)
    return reverse_complement


def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    """
    stop_codons = ['TAG','TAA','TGA']
    for index in range(0, len(dna), 3):
        if dna[index:index+3] in stop_codons:
            dna = dna[:index]
    return dna


def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs_oneframe("CATATGCATATGCATTAGCATCATATGCATTAG")
    ['ATGCATATGCAT', 'ATGCAT']
    """
    index = 0
    orf_list = []
    while index < len(dna)-2:
        if dna[index:index+3] == "ATG":
            orf_list.append(rest_of_ORF(dna[index:]))
            index += len(orf_list[-1])
        else:
            index += 3
    return orf_list


def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAACTGTAG")
    ['ATGCATGAACTG', 'ATGAACTGTAG']
    """
    all_ORFs = []
    for i in range(3): 
        all_ORFs.extend(find_all_ORFs_oneframe(dna[i:]))
    return all_ORFs


def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    both_strands_ORFs = find_all_ORFs(dna)
    both_strands_ORFs.extend(find_all_ORFs(get_reverse_complement(dna)))
    return both_strands_ORFs


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    all_ORFs = find_all_ORFs_both_strands(dna)

    if len(all_ORFs) > 0:
        return max(all_ORFs, key = len)
    else:
        return []
  

def n_longest_ORFs(dna,n):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    all_ORFs = find_all_ORFs_both_strands(dna)

    if len(all_ORFs) > 0:
        return sorted(all_ORFs, key=len)[-n:]
    else:
        return []


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    s = dna

    last_long_ORF = 0

    for i in range(num_trials):
        s = shuffle_string(s)
        if len(longest_ORF(s)) > last_long_ORF:
            last_long_ORF = len(longest_ORF(s))
    return last_long_ORF


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    coding_strand = ''
    for i in range(0, len(dna)-2, 3):
        aa = dna[i:i+3]
        coding_strand += aa_table[aa]
    return coding_strand
        

def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
        
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    threshold = longest_ORF_noncoding(dna, 1500)
    print threshold
    top_ORFs = []
    List_ORFs = find_all_ORFs_both_strands(dna)
    i = -1

    List_ORFs = sorted(L, key=len)
    
    while len(List_ORFs[i]) > threshold:
        top_ORFs.append(coding_strand_to_AA(List_ORFs[i]))
        i -= 1
    return top_ORFs


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    from load import load_seq
    dna = load_seq("./data/X73525.fa")
    print gene_finder(dna)