#!/bin/bash

# Enable the "exit immediately on error" option
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'  # No color

echo -e "${GREEN}Installing MTB++${NC}"
echo "*********************************"
#Checking dependencies are installed
# Check if gcc is installed
exit_flag=0
if which gcc >/dev/null 2>&1; then
  echo -e "${GREEN}gcc is installed.${NC}"
else
  echo -e "${RED}Error: gcc is not installed. Please install it (This software is tested on version 9.3).${NC}"
  exit_flag=1
fi

# Check if python3 is installed
if which python3 >/dev/null 2>&1; then
  echo -e "${GREEN}python3 is installed.${NC}"
else
  echo -e "${RED}Error: python3 is not installed. Please install it.${NC}"
  exit_flag=1

fi 


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

make -C $SBWT_kmer_counter_directory counters -j

echo -e "${GREEN}MTB++ is installed!${NC}"