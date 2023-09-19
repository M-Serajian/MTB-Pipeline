import subprocess
import git
import os
import shutil

installation_error_flag=0


def print_colored_text(text, color):
    if color == "red":
        colored_text = f"\033[31m{text}\033[0m"
    elif color == "green":
        colored_text = f"\033[32m{text}\033[0m"
    elif color == "blue":
        colored_text = f"\033[34m{text}\033[0m"
    else:
        colored_text = text  # No color specified or unsupported color, use default

    print(colored_text)


class RedError(Exception):
    def __init__(self, message):
        super().__init__(f"\033[31m{message}\033[0m")


#working directory 
root_directory = os.getcwd()


import os



#Cloning SBWT_Kmer_counter
SBWT_Kmer_counters_project_name="SBWT-kmer-counters"
SBWT_Kmer_counters_repository_url = "https://github.com/M-Serajian/SBWT-kmer-counters"
SBWT_Kmer_counters_local_directory = root_directory+"/src/SBWT-kmer-counters/"



# Check if the directory exists
if os.path.exists(SBWT_Kmer_counters_local_directory) and os.path.isdir(SBWT_Kmer_counters_local_directory):
    print_colored_text(f"Directory '{SBWT_Kmer_counters_local_directory}' exists and must be removed first!\n","blue")
    # Remove the directory and its contents
    try:
        shutil.rmtree(SBWT_Kmer_counters_local_directory) # Use os.removedirs() if you want to remove parent directories if empty
        print_colored_text(f"Directory '{SBWT_Kmer_counters_local_directory}' removed successfully!\n","green")
        print("******************************************\n")
    except OSError as e:
        message="Error removing directory {}. For the installation, it must be removed. You can remove it manually!\n".format(SBWT_Kmer_counters_local_directory)
        raise RedError(message) from e


# Clone the Git repository

try:
    repo = git.Repo.clone_from(SBWT_Kmer_counters_repository_url, SBWT_Kmer_counters_local_directory)
    message="Successfully cloned {} to {}".format(SBWT_Kmer_counters_repository_url, SBWT_Kmer_counters_local_directory)
    print("\033[32m{}\033[0m\n".format(message))
    print("******************************************\n")
except OSError as e:
    message="Could not clone {} from github!\n".format(SBWT_Kmer_counters_repository_url)
    raise RedError(message) from e



# SBWT compilation
os.chdir(SBWT_Kmer_counters_local_directory)
process=subprocess.run("git submodule update --init --recursive",shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
for line in process.stdout:
    print(line, end='')         


SBWT_build_directory=SBWT_Kmer_counters_local_directory+"SBWT/build/"

process=subprocess.Popen(["cmake", "..", "-DCMAKE_BUILD_ZLIB=1"], cwd=SBWT_build_directory)

process=subprocess.Popen(["make -j>errors.log"], cwd=SBWT_build_directory)

