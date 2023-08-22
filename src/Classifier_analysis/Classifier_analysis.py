import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the saved model

Cross_Validation=5

Drug_names=["Isoniazid",
            "RIA",
            "Rifabutin",
            "Rifabutin",
            "Ethambutol",
            "FQS",
            "Ethionamide",
            "Levofloxacin",
            "Moxifloxacin",
            "AMG",
            "Kanamycin",
            "Amikacin",
            "Clofazimine",
            "Delamanid",
            "Linezolid",
            "Bedaquiline"]

Top_kmers_model=[1024,
                 16384,
                 4096,
                 1024,
                 16384,
                 1024,
                 16384,
                 256,
                 1024,
                 4096,
                 4096,
                 4096,
                 1024,
                 262144,
                 262144,
                 262144]


base_address="/blue/boucher/share/Deep_TB_Ali/Final_TB/Saved_classifier/Cross_Validation_"+str(Cross_Validation)+"/"
for i in range(np.size(Top_kmers_model)):
    model_address=base_address+"LR_{}_{}.pkl".format(Drug_names[i],str(Top_kmers_model[i]))
    loaded_model = joblib.load(model_address)
    coefficients = loaded_model.coef_[0]
    non_zero_count = np.count_nonzero(coefficients)
    #print("LR :"+Drug_names[i]+str(":")+str(non_zero_count))

    model_address=base_address+"RF_{}_{}.pkl".format(Drug_names[i],str(Top_kmers_model[i]))
    loaded_model = joblib.load(model_address)
    feature_importances = loaded_model.feature_importances_
    # Count the number of effective features
    effective_features_count = sum(importance > 0 for importance in feature_importances)
    print(effective_features_count)
    