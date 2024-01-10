#!/usr/bin/perl
use strict;
use warnings;

# Process arguments to check for help flag
foreach my $arg (@ARGV) {

    if ($arg eq '-h' || $arg eq '--help') {

        system("python /src/31mer_analysis/31mer_analysis_multi_thread.py -h");

        exit 0;
    }
}

# Construct the command to call the Python script with the original arguments
my $command = "python src/31mer_analysis/31mer_analysis_multi_thread.py " . join(' ', @ARGV);

# Execute the command and show output
my $exit_status = system($command);

# Check if the execution was successful
$exit_status >>= 8; # Get the actual exit status

if ($exit_status == 0) {
    print "The 31mer analysis is finished!\n";

} else {

    print "Error in src/31mer_analysis/31mer_analysis.py/31mer_analysis_multi_thread.py execution with exit status $exit_status.\n";
    print "For debug, please report this in the issue section of the MTB++ software, thank you!"

}