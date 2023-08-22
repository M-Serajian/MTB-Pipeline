#!/usr/bin/env python
import time
import numpy as np
import sys

file_number=int(sys.argv[1])
Color_matrix_address=sys.argv[3]
Npy_files_address=sys.argv[4]
Number_of_Samples=int(sys.argv[2])
Number_of_kmers_in_file=int(sys.argv[5])
min_Filter=int(sys.argv[6])
max_Filter=int(sys.argv[7])




"""  Old version without the kmer index 

def line_parser (string,number_of_samples):
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

    return binary_output, occurance_counter
"""

# Kmer index is added now, its the first element (index zero)
def line_parser (string,number_of_samples):
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
    binary_output.append(int(string[0:list1[0]-1])) # This is index of the kmer which is at the end of each array _ the size will be 6225, in which the first 6224 ones are the mains and the last is kmer index
    return binary_output, occurance_counter


def main():

    print("file_number is {}".format(file_number),flush=True)
    print("Color_matrix_address is {}".format(Color_matrix_address),flush=True)
    print("Npy_files_address is {}".format(Npy_files_address),flush=True)
    print("Number_of_Samples is {}".format(Number_of_Samples),flush=True)
    print("Number_of_kmers_in_file is {}".format(Number_of_kmers_in_file),flush=True)
    print("Filter is {}".format(min_Filter),flush=True)
    print("Filter is {}".format(max_Filter),flush=True)


    base_address= Npy_files_address
    color_matrix_file = open(Color_matrix_address,"r")
    
    output_array=[]
    start_number= (file_number-1)  *  Number_of_kmers_in_file
    end_number  = file_number         *  Number_of_kmers_in_file
    line_number=-1 #Line number starts form zero

    Ten_percent_loop= start_number + int(0.1*(end_number - start_number))
    print("Ten_percent_loop is {}".format(Ten_percent_loop),flush=True)
    print("The type of Ten_percent_loop is {}".format(type(Ten_percent_loop)),flush=True)
    

    for line in color_matrix_file:
        line_number= line_number+1
        

        if (line_number==start_number): 
            t1=time.time()

        if (line_number==Ten_percent_loop): 
            t2=time.time()
            print("Ten Percernt is done! in {} sec".format(round((t2-t1),2)),flush=True)

        if (start_number<line_number and line_number<=end_number):

            occurance=line.count(":")

            if  (min_Filter <occurance and occurance < max_Filter):
                binary, _=line_parser(line, Number_of_Samples)
                output_array.append(binary)

        if (end_number < line_number):
            break

    #List to array
    output_array=np.array(output_array)

    print("the shape of the array in .NPY is {}".format(np.shape(output_array)),flush=True)

    np.save(base_address+"counts_file{}.npy".format(file_number),output_array)

    color_matrix_file.close()
    print("the shape of the array in .NPY is {}".format(np.shape(output_array)))
    print("Finished succesfully!")
    t3=time.time()
    print("The total time used is: {} secs".format(round(t3-t1),2))


if  __name__ == '__main__' :
    main()