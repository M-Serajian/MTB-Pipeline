import os
from Bio import SeqIO
import gzip
import concurrent.futures
import linecache

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    return lines



def get_line(file_path, line_number):
    line = linecache.getline(file_path, line_number)
    return line.strip()

def Counter(gz_file_address):
    

    parent_dir, sub_dir = os.path.split(gz_file_address)
    second_parent_dir, second_sub_dir = os.path.split(parent_dir)
    count1 = 0
    count2 = 0

    file1=gz_file_address+ "{}_1.fastq.gz".format(second_sub_dir)
    file2=gz_file_address+ "{}_2.fastq.gz".format(second_sub_dir)


    with gzip.open(file1, "rt") as handle:
        for record in SeqIO.parse(handle, "fastq"):
            count1 += 1
    with gzip.open(file2, "rt") as handle:
        for record in SeqIO.parse(handle, "fastq"):
            count2 += 1
    
    print([second_sub_dir,count1,count2,count1 + count2])
    return [second_sub_dir,count1,count2,count1 + count2]


# Specify the file path
file_path = 'input_fastq_list.txt'  # Replace with the path to your text file
# Read the file and store the lines as a list
lines_list = read_file(file_path)
# Create a ThreadPoolExecutor with the desired number of threads
num_threads = 20  # Choose the number of threads you want to use
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Submit the function to the executor for execution 20 times
    futures = [executor.submit(Counter(lines_list[i])) for i in range(20)]

    # Get the results from each thread
    output_list = []
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        output_list.append(result)

print(output_list)


