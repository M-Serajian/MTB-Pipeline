# This code is designed to devide data to different number of folds
# to be further used for cross validation
number_of_samples=6224
number_of_folds=5
saving_address=/blue/boucher/share/Deep_TB_Ali/Cross-validation-indexes/
ml python
chmod a+x projects/MTB-plus-plus/src/Cross-validation_fold_creation.py
python projects/MTB-plus-plus/src/Cross-validation_fold_creation.py \
       $number_of_samples\
       $number_of_folds\
       $saving_address