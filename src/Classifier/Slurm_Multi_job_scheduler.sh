#!/bin/bash
#This code creates 16 different .sh files each related to
#one of the specific drugs that would be further given to hypergator
#This code is to ensure the name of job array for each of the 
#drugs is based on the true name of the drug. (look line 31 and 46 in this code)
#This will be very useful for tracking logs and later debugs
# Modify from here:

Cross_Validation=5
Needed_memory=80gb
Process_time=60:00:00
Array_job_list=1-1 # single job: For each Classifer, We considered one Job
Main_job_action_name=Classifer
email=ms.slurm@gmail.edu

#____________________________________________#
drugs=("Amikacin" \
        "Bedaquiline" \
        "Clofazimine" \
        "Delamanid" \
        "Ethambutol" \
        "Ethionamide" \
        "Isoniazid" \
        "Kanamycin" \
        "Levofloxacin" \
        "Linezolid" \
        "Moxifloxacin" \
        "Rifampicin" \
        "Rifabutin" \
        "RIA" \
        "AMG" \
        "FQS")

mkdir -p temp
mkdir -p temp/logs   #for saving the logs



for ((i=0; i<=15; i++))
do
    job_name="Classifier_"${drugs[i]}
    drug_name=${drugs[i]}

    Top_kmers_for_each_drug_address=/blue/boucher/share/Deep_TB_Ali/Final_TB/Top_kmers_for_each_drug/Cross_validation_$Cross_Validation/
    train_index_address="/blue/boucher/share/Deep_TB_Ali/Final_TB/test_train_index/Cross_validation_$Cross_Validation/train_index_CV$Cross_Validation.npy"
    test_index_address="/blue/boucher/share/Deep_TB_Ali/Final_TB/test_train_index/Cross_validation_$Cross_Validation/test_index_CV$Cross_Validation.npy"
    Results_address="/home/m.serajian/Final_TB/Deep_TB/classifier/Cross_Validation_"$Cross_Validation"_results/"
    Saving_Model_Address="/blue/boucher/share/Deep_TB_Ali/Final_TB/Saved_classifier/Cross_Validation_"$Cross_Validation"/"

    # Generate the Slurm script dynamically using a heredoc
cat << EOF > ./temp/$job_name.sh
#!/bin/bash
#SBATCH --job-name=$job_name
#SBATCH --mail-type=ALL            # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=$email   # Where to send mail
#SBATCH --ntasks=1                       # Run a single task
#SBATCH --mem=$Needed_memory                        # Job Memory
#SBATCH --time=$Process_time                 # Time limit hrs:min:sec
#SBATCH --array=$Array_job_list                  # Array range
#SBATCH --output=temp/logs/"$Main_job_action_name"_%A_%a_$drug_name_group.log

ml python3
chmod a+x classifier.py       


mkdir -p $Results_address
mkdir -p $Saving_Model_Address

/usr/bin/time -f "Time: %U user, %S system, %e real\nMemory: %M" \
                ./classifier.py ${drug_name} $Top_kmers_for_each_drug_address \
                 $Results_address $Cross_Validation $train_index_address $test_index_address\
                 $Saving_Model_Address

EOF

    sbatch ./temp/$job_name.sh

    echo Classifier for ${drug_name} submitted!
    
done