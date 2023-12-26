#!/usr/bin/env ruby
require 'csv'
require 'optparse'

# ANSI color codes for print
red_color = "\033[91m"
blue_color = "\033[94m"
green_color = "\033[92m"
reset_color = "\033[0m"

def get_csv_files(data_directory)
  # Get a list of CSV files in the data directory
  csv_files = Dir.entries(data_directory).select { |file| file.downcase.end_with?('.csv') }

  if csv_files.empty?
    error_message = "#{red_color}No CSV files found in the data directory: #{data_directory}. There are no MTB++ reports available.#{reset_color}"
    puts error_message
    raise Errno::ENOENT, error_message
  end

  # Return base names without the '.csv' extension
  csv_files.map { |file| File.basename(file, '.csv') }
end

def validate_directories(data_directory, output_directory)
  # Validate data directory
  unless File.directory?(data_directory)
    puts "Error: Data directory '#{data_directory}' does not exist."
    exit(1)
  end

  # Validate output directory
  unless File.directory?(output_directory)
    puts "Error: Output directory '#{output_directory}' does not exist."
    exit(1)
  end
end

# Finding the reports of MTB++
def MTBpp_report(csv_file_path, model)
    CSV.foreach(csv_file_path) do |row|
      return row[1..-1] if row[0] == model
    end
  
    # Return nil if the target value is not found
    nil
  end
  

def process_mtb_results(data_directory, output_directory, input_data)
  # List to store data
  lr_predictions = []
  rf_predictions = []
  csv_header = ['Genome ID', 'Amikacin', 'Bedaquiline', 'Clofazimine', 'Delamanid', 'Ethambutol', 'Ethionamide',
                'Isoniazid', 'Kanamycin', 'Levofloxacin', 'Linezolid', 'Moxifloxacin', 'Rifampicin', 'Rifabutin',
                'RIA', 'AMG', 'FQS']

  lr_predictions << csv_header
  rf_predictions << csv_header

  # Iterate through Genome IDs in the input CSV file
  input_data.each do |genome_id|
    file_path = File.join(data_directory, "#{genome_id}.csv")

    if File.exist?(file_path)
      lr_prediction = MTBpp_report(file_path, "Logistic Regression")
      lr_predictions << [genome_id] + lr_prediction

      rf_prediction = MTBpp_report(file_path, "Random Forest")
      rf_predictions << [genome_id] + rf_prediction
    end
  end

  # Write the consolidated data to a single output CSV file
  lr_output = File.join(output_directory, 'MTB++_Logistic Regression.csv')
  CSV.open(lr_output, 'w') { |csv| lr_predictions.each { |row| csv << row } }

  rf_output = File.join(output_directory, 'MTB++_Random Forest.csv')
  CSV.open(rf_output, 'w') { |csv| rf_predictions.each { |row| csv << row } }

  puts "Report CSV files are available at: #{output_directory}"
end

def main
  # Argument parser
  options = { output_directory: '.' }

  OptionParser.new do |opts|
    opts.banner = 'Usage: MTB++_report.rb -d DATA_DIRECTORY [-o OUTPUT_DIRECTORY]'
  
    opts.on('-d', '--data-directory DATA_DIRECTORY', 'Directory where the MTB++ results are stored.') do |data_directory|
      options[:data_directory] = data_directory
    end
  
    opts.on('-o', '--output-directory [OUTPUT_DIRECTORY]', 'Directory to save the consolidated CSV file. Default is current directory.') do |output_directory|
      options[:output_directory] = output_directory || '.' # Use '.' as default if not provided
    end
  end.parse!

  # Validate directories
  validate_directories(options[:data_directory], options[:output_directory])

  # Finding the reports
  input_data = get_csv_files(options[:data_directory])
  # Process MTB++ results and create the consolidated CSV file
  process_mtb_results(options[:data_directory], options[:output_directory], input_data)
end

if __FILE__ == $PROGRAM_NAME
  main
end
