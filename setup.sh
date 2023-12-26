#!/bin/bash

# Enable the "exit immediately on error" option
set -e
# defining colors for readability
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'  # No color

echo -e "${GREEN}Installing MTB++${NC}"
echo "******************************************************************"
#Checking dependencies are installed

# ------------------ GCC ------------------
# Check if gcc is installed
exit_flag=0
if which gcc >/dev/null 2>&1; then
  echo -e "${GREEN}gcc is installed.${NC}"
else
  echo -e "${RED}Error: gcc is not installed. Please install it (This software is tested on version 9.3).${NC}"
  exit_flag=1
fi



# ------------------ Cmake ------------------
# First loading cmake
module load cmake 

# Check if cmake is installed
if which cmake >/dev/null 2>&1; then
  echo -e "${GREEN}cmake is installed.${NC}"
else
  echo -e "${RED}Error: cmake is not installed. Please install it.${NC}"
  exit_flag=1
fi

if [ "$exit_flag" = "1" ]; then
    echo -e "${RED} Please install the dependencies first!${NC}"
    exit 1
fi



# ------------------ SBWT kmer counters ------------------
#root directory
root_directory=$(pwd)

# Check if the directory exists
SBWT_kmer_counter_directory="$root_directory/src/SBWT-kmer-counters"

# Checking the SBWT-kmer-counter is empty to clone the repository with no errors
if [ -d $SBWT_kmer_counter_directory ]; then

    echo -e "\e[32mSBWT-kmer-counters directory exists. Removing it ...\e[0m"

    rm -rf "$SBWT_kmer_counter_directory"

    echo -e "\e[34mSBWT-kmer-counters directory removed!\e[0m"

fi

echo -e "\e[32mCloning and compiling BWT-kmer-counters\e[0m"

sleep 2

git clone https://github.com/M-Serajian/SBWT-kmer-counters.git \
    $SBWT_kmer_counter_directory

git -C $SBWT_kmer_counter_directory submodule update --init --recursive

SBWT_directory="$SBWT_kmer_counter_directory/SBWT/"

SBWT_build_directory="$SBWT_directory/build"

cmake -B $SBWT_build_directory -S $SBWT_directory -DCMAKE_BUILD_ZLIB=1

make -C $SBWT_build_directory -j

make -C $SBWT_kmer_counter_directory -j



# ------------------ Python3 ------------------

# Check if python3 is installed
if which python3 >/dev/null 2>&1; then
  echo -e "${GREEN}python3 is installed.${NC}"
else
  echo -e "${RED}Error: python3 is not installed. Please install it.${NC}"
  exit_flag=1

fi 
module load python

# ------------------ scikit_learn ------------------

# Desired scikit-learn version
desired_version_scikit_learn="1.1.2"

# Check if scikit-learn is installed
if python -c "import sklearn" >/dev/null 2>&1; then
    echo -e "${GREEN}Scikit-learn is already installed${NC}"
else
    echo -e "${RED}Scikit-learn is not installed. Installing version $desired_version_scikit_learn${NC}"
    pip3 install scikit-learn==$desired_version_scikit_learn
fi

# Check scikit-learn version
current_version_scikit_learn=$(python -m pip show scikit-learn | grep Version | awk '{print $2}')

echo "Current scikit-learn version: $current_version_scikit_learn"

# Check if the version is already 1.1.2
if [ "$current_version_scikit_learn" = "$desired_version_scikit_learn" ]; then
    echo -e "${GREEN}Scikit-learn is already version $desired_version_scikit_learn${NC}"
else
    # Update scikit-learn to 1.1.2
    pip install --upgrade scikit-learn==$desired_version_scikit_learn

    # Check if the update was successful
    updated_version_scikit_learn=$(python -m pip show scikit-learn | grep Version | awk '{print $2}')
    if [ "$updated_version_scikit_learn" = "$desired_version_scikit_learn" ]; then
        echo -e "${GREEN}Scikit-learn successfully updated to version $desired_version_scikit_learn${NC}"
    else
        echo -e "${RED}Error: Scikit-learn could not be updated to version $desired_version_scikit_learn${NC}"
        exit 1  # Abort the program
    fi
fi


echo -e "${GREEN}MTB++ is installed!${NC}"