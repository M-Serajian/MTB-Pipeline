import subprocess

#Cloning SBWT_Kmer_counter
repository_url = "https://github.com/M-Serajian/SBWT-kmer-counters"
local_directory = "/src/"
subprocess.run(["git", "clone", repository_url, local_directory], check=True)