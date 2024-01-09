#!/usr/bin/perl
use strict;
use warnings;

# Process arguments to check for help flag
foreach my $arg (@ARGV) {
    if ($arg eq '-h' || $arg eq '--help') {
        system("python 31mer_analysis.py -h");
        exit 0;
    }
}

# Construct the command to call the Python script with the original arguments
my $command = "python 31mer_analysis.py " . join(' ', @ARGV);

# Execute the command and show output
my $exit_status = system($command);

# Check if the execution was successful
$exit_status >>= 8; # Get the actual exit status

if ($exit_status == 0) {
    print "Successfully done.\n";
} else {
    print "Error in 31mer_analysis.py execution with exit status $exit_status.\n";
}
