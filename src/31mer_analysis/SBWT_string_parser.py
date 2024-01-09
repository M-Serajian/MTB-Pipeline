#!/usr/bin/env python

def line_parser (string):
    count = string.count("(")
    first_paranthesis_index = string.find("(")
    
    kmer_index=int(string[0:first_paranthesis_index-1]) # This is index of the kmer which is at the end of each array _ the size will be 6225, in which the first 6224 ones are the mains and the last is kmer index
    return count, kmer_index

