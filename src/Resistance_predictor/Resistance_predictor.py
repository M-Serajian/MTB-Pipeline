import numpy as np
import joblib
import os
from .utils import Ascii_reader

# Drug_number, orders 
drug_names=["Amikacin",\
            "Bedaquiline",\
            "Clofazimine",\
            "Delamanid",\
            "Ethambutol",\
            "Ethionamide",\
            "Isoniazid",\
            "Kanamycin",\
            "Levofloxacin",\
            "Linezolid",\
            "Moxifloxacin",\
            "Rifampicin",\
            "Rifabutin",\
            "RIA",\
            "AMG",\
            "FQS"]


def AMR_predictor(SBWT_ascci_output_address,drug_number):
    output=[]

    drug=drug_names[drug_number]
    
    #Transforming SBWT to a matrix readable for machine learning
    exteracted_features=Ascii_reader.ml_readable_matrix_generator(SBWT_ascci_output_address,drug_number)

    #loading trained model
    LR_model_path = os.path.join('..', '..','data',"trained_models", '{}_LR.pkl'.format(drug))
    loaded_model = joblib.load(LR_model_path)

    number_of_features_needed=np.size(loaded_model.coef_)
    exteracted_features_for_ml=exteracted_features[:,:number_of_features_needed]

    prediction=loaded_model.predict(exteracted_features_for_ml)[0]

    if (prediction==0):
        output.append("Susceptible")
        
    else:
        output.append("Resistant")


    RF_model_path = os.path.join('..', '..','data',"trained_models", '{}_RF.pkl'.format(drug))
    loaded_model = joblib.load(RF_model_path)

    number_of_features_needed=np.size(loaded_model.feature_importances_)
    exteracted_features_for_ml=exteracted_features[:,:number_of_features_needed]

    prediction=loaded_model.predict(exteracted_features_for_ml)[0]

    if (prediction==0):
        output.append("Susceptible")
        
    else:
        output.append("Resistant")

    return(output)
