#!/usr/bin/env python
import numpy as np
import os
import joblib
#list of Drugs


def line_parser (string):
    
    number_of_samples=1 # Only one single fastafile as input is allowed
    list1 = []
    list2 = []
    list3 = []

    for i in range(len(string)):

        if string[i] == "(":
            list1.append(i)
    occurance_counter=len(list1)

    for i in range(len(string)):

        if string[i] == ":":
            list2.append(i)

    for i in range(len(string)):

        if string[i] == ")":
            list3.append(i)

    binary_output = [0] * number_of_samples

    for i in range (len(list1)):

        a = int(string[list1[i] + 1:list2[i]])

        binary_output[a]= int(string[list2[i] + 1:list3[i]])

    sbwt_index_rank=(int(string[0:list1[0]-1])) # This is index of the kmer which is at the end of each array _ the size will be 6225, in which the first 6224 ones are the mains and the last is kmer index
    #print(occurance_counter)
    return sbwt_index_rank, binary_output[0]


def SBWT_Matrix_creator(address_to_ascii_file,length_of_array):

    output_array_sbwt_rank = [0] * length_of_array

    # Open the file in read mode
    with open(address_to_ascii_file, 'r') as file:
        # Read and print each line one by one
        for line in file:

            [rank,occurance]= line_parser(line)

            output_array_sbwt_rank[rank]=occurance
        
    return(output_array_sbwt_rank) 



def sbwt_rank_to_trained_ml_rank(input_sbwt_rank_array,group_number):

    data_file_path = os.path.join('..','..', '..',\
                                  'data',"SBWT_hash_table",\
                                  'SBWT_index_to_Top_kmer_transform_matrix.npy')

    full_transform_array=np.load(data_file_path)

    transform_array=full_transform_array[:,group_number]

    output_array=[0]*65536  # 2^17 features are exteracted

    for i in range (np.size(output_array)):

        output_array[i]=input_sbwt_rank_array[transform_array[i]]

    return output_array




# Wrapper function:              ex. output of sbwt               
def ml_readable_matrix_generator(SBWT_Kmer_orders_drug_address, drug_number):
    
    Number_of_feature=200000 # Any number over 200000 works (This is due to the fact that SBWT indexes are in this range)

    SBWT_matrix=SBWT_Matrix_creator(SBWT_Kmer_orders_drug_address,Number_of_feature)

    Ml_readable_matrix=sbwt_rank_to_trained_ml_rank(SBWT_matrix,drug_number)

    output_size=np.size(Ml_readable_matrix)

    Ml_readable_matrix=np.array(Ml_readable_matrix)

    Ml_readable_matrix=Ml_readable_matrix.reshape(1,output_size)

    return (Ml_readable_matrix)

