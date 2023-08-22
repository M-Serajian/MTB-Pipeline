#!/usr/bin/env python
import sys
import time
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt


from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.datasets import load_iris


import pickle





def get_non_nan_indices(array):
    non_nan_indices = []
    for i in range(len(array)):
        if not np.isnan(array[i]):
            non_nan_indices.append(i)
    return non_nan_indices


# Argument 1: drug name
# 
# Loading Targets
drug_name_group=sys.argv[1]
Top_kmers_address=sys.argv[2]
Results_address=sys.argv[3]
Cross_Validation=sys.argv[4]
train_index_address=sys.argv[5]
test_index_address=sys.argv[6]
model_address=sys.argv[7]

train_index=np.load(train_index_address)
test_index=np.load(test_index_address)

df=pd.read_csv("6224_Targets_NA_3_letters.csv")

print("Columns in the CSV file are:",flush=True)
print(df.columns,flush=True)

drug_names=['ERR', 'ID', 'ERS',"Amikacin",\
            "Bedaquiline", "Clofazimine",\
            "Delamanid","Ethambutol", "Ethionamide",\
            "Isoniazid", "Kanamycin","Levofloxacin",\
            "Linezolid","Moxifloxacin", "Rifampicin",\
            "Rifabutin","RIA","AMG","FQS"]




try:
  CSV_index = drug_names.index(drug_name_group)
except Exception as error:
  raise ValueError("Could not find the drug name; \
                   The drug names are: \n \
                   Amikacin ,\n \
                   Bedaquiline ,\n \
                   Clofazimine,\n \
                   Delamanid ,\n \
                   Ethambutol ,\n \
                   Ethionamide ,\n \
                   Isoniazid ,\n \
                   Kanamycin ,\n \
                   Levofloxacin ,\n \
                   Linezolid ,\n \
                   Moxifloxacin ,\n \
                   Rifampicin ,\n \
                   Rifabutin ,\n \
                   RIA ,\n \
                   AMG ,\n \
                   FQS ")

print("Drug Found!",flush=True)


# Columns of the target file are: 
#IDX:0      1     2      3      4      5      6
# ['ERR', 'ID', 'ERS', 'AMI', 'BDQ', 'CFZ', 'DLM',
# 'EMB', 'ETH', 'INH','KAN', 'LEV', 'LZD', 'MXF',
# 'RIF', 'RFB', 'RIFBB'='RIA', 'Ami_Kan'='AMG','Fluoroquinolone'='FQS']

drug_names_abbreviations=['ERR', 'ID', 'ERS',"AMI",\
            "BDQ", "CFZ",\
            "DLM","EMB", "ETH",\
            "INH", "KAN","LEV",\
            "LZD","MXF", "RIF",\
            "RFB","RIA","AMG","FQS"]


group=CSV_index 
print("Column number on CSV is {}".format(group),flush=True)
drug_name=drug_names[group]
drug_names_abbreviation=drug_names_abbreviations[group]

print("The drug is : {}".format(drug_name),flush=True)
target=np.array(df)
print("The shape of the target is:",flush=True)
print(np.shape(target),flush=True)
phenotype=target[:,group]


# Loading data
data=np.load(Top_kmers_address+ drug_name+ "/Classifer_data_524288.npy")
print("The data is loaded",flush=True)

# loading clade
"""
clade=np.load("/blue/boucher/share/Deep_TB_Ali/Extracted_kmer_true_targets/Clade_counts.npy")

data=np.hstack((data,np.reshape(clade,(np.size(clade),1))))

print("Clade is added!")
print("The shape of the data is : {}".format(np.shape(data)))
"""

print("train data size is: {}\n".format(np.shape(train_index)),flush=True)
print("test data size is: {}\n".format(np.shape(test_index)),flush=True)


y_train=phenotype[train_index]
non_ambiguous_indecies_y_train=get_non_nan_indices(y_train)
train_index=train_index[non_ambiguous_indecies_y_train]
phenotype=target[:,group]
y_train=phenotype[train_index]
y_train=y_train.astype('int')

print("Number of R in train set is after ambiguity removal: {}".format(np.sum(y_train)),flush=True)
y_test =phenotype[test_index]
non_ambiguous_indecies_y_test=get_non_nan_indices(y_test)
test_index=test_index[non_ambiguous_indecies_y_test]
y_test =phenotype[test_index]
y_test=y_test.astype('int')


print("Number of R in test set is: {}".format(np.sum(y_test)),flush=True)
X_train=data[train_index,:]
X_test=data[test_index,:]



plt.axis("square")
plt.xlabel("False Positive Rate",fontsize=16)
plt.ylabel("True Positive Rate",fontsize=16)
#plt.title(drug_names_abbreviation,fontsize=22)

header_csv=["Model", "Kmers used","Learning time (S)","AUC(%)","ACC(%)","Sensitivity(%)","Specificity(%)","F-1 Score"]
csv_file=[]
base=4 # 1 kmers, base kmers, base^2 kmers, base^3 kmers , ...
list_kmers=[1* pow(base,i) for i in range(math.ceil(math.log(((np.size(X_train,1))/1),base)))]
#list_kmers.append(np.size(X_train,1))

colors = ['#006400', '#228B22', '#808000', '#00FF00', '#00FF7F',
          '#2E8B57', '#98FB98', '#7FFF00', '#98FB98', '#50C878']

color_counter=0
#Logistic Regression

LR=1
if (LR==1):
  for i in list_kmers :

    if ( 1000<i):
      model=LogisticRegression(penalty='l1', solver='liblinear', max_iter=2000)
      model_name="LR Lasso"
    else: 
      model=LogisticRegression(max_iter=2000)
      model_name="LR"
    
    print("{} model with {} Kmers".format(model_name,i),flush=True) 

    X_train_selected= X_train[:,0:i]
    X_test_selected=X_test[:,0:i]
    t1=time.time()
    clf = model.fit(X_train_selected, y_train)
    t2=time.time()

    #Saving the model
    saving_model_address=model_address+'LR_{}_{}.pkl'.format(drug_name,i)

    with open(saving_model_address, 'wb') as f:
        pickle.dump(clf, f)
    

    y_pred = clf.predict(X_test_selected)
    #print("For i= {} the ACC and Pr. and Rec. are :".format(i))
    accuracy = accuracy_score(y_test, y_pred)
    conf = confusion_matrix(y_test, y_pred)

    tn, fp, fn, tp=conf.ravel()
    specificity= tn / (tn + fp)
    sensitivity= tp / (tp + fn)

    f1 = f1_score(y_test, y_pred)

    fpr, tpr, thresholds = metrics.roc_curve(y_test,\
                          model.predict_proba(X_test_selected)[:,1])
    auc = metrics.roc_auc_score(y_test,model.predict(X_test_selected))
    plt.plot(fpr, tpr,label= model_name+ " {} Kmers "\
            .format(i), color=colors[color_counter])
    color_counter=color_counter+1
    
    csv_file.append([model_name, i, round(t2-t1,2),\
                    round(100*auc,2), round(100*accuracy,2),\
                    round(100*sensitivity,2), round(100*specificity,2),\
                    round(100*f1,2)])




colors = ['#8B0000', '#800000', '#A52A2A', '#B22222', '#DC143C',
          '#FF0000', '#FF6347', '#FF7F50', '#FA8072', '#FFA07A']
color_counter=0

# Random forest (RF)
RF=1

if (RF==1):
   
  for i in list_kmers :
    model_name="RF"
    print("{} model with {} Kmers".format(model_name,i),flush=True) 
    model = RandomForestClassifier(max_depth=10, random_state=10)

    X_train_selected= X_train[:,0:i]
    X_test_selected=X_test[:,0:i]
    t1=time.time()
    clf = model.fit(X_train_selected, y_train)
    t2=time.time()

    saving_model_address=model_address+'RF_{}_{}.pkl'.format(drug_name,i)

    with open(saving_model_address, 'wb') as f:
        pickle.dump(clf, f)

    y_pred = clf.predict(X_test_selected)
    #print("For i= {} the ACC and Pr. and Rec. are :".format(i))
    accuracy = accuracy_score(y_test, y_pred)
    conf = confusion_matrix(y_test, y_pred)

    tn, fp, fn, tp=conf.ravel()
    specificity= tn / (tn + fp)
    sensitivity= tp / (tp + fn)

    f1 = f1_score(y_test, y_pred)

    fpr, tpr, thresholds = metrics.roc_curve(y_test,\
                          model.predict_proba(X_test_selected)[:,1])
    auc = metrics.roc_auc_score(y_test,model.predict(X_test_selected))
    plt.plot(fpr, tpr,label= model_name+ " {} Kmers "\
            .format(i), color=colors[color_counter])
    color_counter=color_counter+1
    csv_file.append([model_name, i, round(t2-t1,2),\
                    round(100*auc,2), round(100*accuracy,2),\
                    round(100*sensitivity,2), round(100*specificity,2),\
                    round(100*f1,2)])


SVM_RBF=0

if (SVM_RBF==1):
   
  for i in list_kmers :

    X_train_selected= X_train[:,0:i]
    X_test_selected=X_test[:,0:i]
    """
    if ( 1000<i):
      model_name="SVM RBF PCA"
      print("{} model with {} Kmers and Top 256 Components ".format(model_name,i),flush=True) 
      pca = PCA(n_components=256)
      pca.fit(X_train_selected)

      # Transform the training and test data
      X_train_selected = pca.transform(X_train_selected)
      X_test_selected = pca.transform(X_test_selected)
            
    else: 
      model_name="SVM RBF"
      print("{} model with {} Kmers".format(model_name,i),flush=True) 
    """
    print("{} model with {} Kmers".format(model_name,i),flush=True)
    model_name="SVM RBF"
    model=SVC(kernel='rbf',max_iter=1000,probability=True)

    t1=time.time()
    clf = model.fit(X_train_selected, y_train)
    t2=time.time()

    y_pred = clf.predict(X_test_selected)
    #print("For i= {} the ACC and Pr. and Rec. are :".format(i))
    accuracy = accuracy_score(y_test, y_pred)
    conf = confusion_matrix(y_test, y_pred)

    tn, fp, fn, tp=conf.ravel()
    specificity= tn / (tn + fp)
    sensitivity= tp / (tp + fn)

    f1 = f1_score(y_test, y_pred)

    fpr, tpr, thresholds = metrics.roc_curve(y_test,\
                          model.predict_proba(X_test_selected)[:,1])
    auc = metrics.roc_auc_score(y_test,model.predict(X_test_selected))

    plt.plot(fpr, tpr,label= model_name+ " {} Kmers "\
            .format(i), color=colors[color_counter])
    
    color_counter=color_counter+1
    csv_file.append([model_name, i, round(t2-t1,2),\
                    round(100*auc,2), round(100*accuracy,2),\
                    round(100*sensitivity,2), round(100*specificity,2),\
                    round(100*f1,2)])

   

   




plt.rcParams["figure.figsize"] = [8, 8]
plt.rcParams["figure.autolayout"] = True
plt.rcParams["figure.dpi"] = 350
plt.xlim(0,1)
plt.ylim(0,1)
plt.plot([0, 1], [0, 1], "k--", label="(AUC = 0.5)")
#plt.legend(loc='center', bbox_to_anchor=(1.4, 0.5),fontsize=10)
#plt.legend(bbox_to_anchor=(1.3, 0.8),loc='upper left')
#plt.subplots_adjust(right=0.6)

#plt.subplots_adjust(left=0, right=1, top=1.1, bottom=0)
plt.xticks(fontsize=14)  # Adjust the font size for x-axis tick labels
plt.yticks(fontsize=14)  # Adjust the font size for y-axis tick labels
plt.savefig(Results_address+drug_names_abbreviation+'_CV{}_ROC.jpg'.format(Cross_Validation),bbox_inches='tight')
plt.show()


pd.DataFrame(csv_file).to_csv(Results_address+drug_names_abbreviation+\
                              '_CV{}.csv'.format(Cross_Validation), index_label = "MLs",\
                              header= header_csv)


print("Classification for {} finished Successfully!".\
      format(drug_name))




   