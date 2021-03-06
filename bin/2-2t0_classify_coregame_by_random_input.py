#%%
import pandas as pd
import pickle
import numpy as np
import seaborn
import matplotlib.pyplot as plt

import gensim
import sklearn.decomposition
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestRegressor
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import KFold

import warnings
#Ignore all warnings
warnings.simplefilter('ignore', category=Warning)


#%%
#--Read in data
#Remember to expand the review
df_core = pickle.load(open(r'..\data\process\core_cluster.p', 'rb'))
df = pickle.load(open(r'..\data\process\score_10_doc2vec.p', 'rb')) #The smallest df


#%%
#--Core game group label
idTags = []
groups = []
for index, row in df.iterrows():
    if row['CoreID'] > 0:
        idTag = 'id_' + str(index)
        group = (df_core[df_core['core_id'] == row['CoreID']])['group_label'].values[0]

        idTags.append(idTag)
        groups.append(group)


#%%
#--Get core game vecs and organize into a df
#The first "group" is coregame cluster tag; "groupn" is the distance between each doc and keyword group centroid
df_core_expand = pd.DataFrame({
    'idTag': idTags,
    'group': groups,
})

#Core game vecs
keyGNum = 300
np.random.seed(4)
coreVecs = pd.DataFrame(np.random.rand(len(df_core_expand), keyGNum))
pd.DataFrame(coreVecs)

#Make into a df
df_core_expand = pd.merge(df_core_expand.reset_index(drop=True), coreVecs.reset_index(drop=True), left_index=True, right_index=True)
numOfCluster = len(df_core_expand.group.unique())


#%%
#--K fold setting up
kf = KFold(n_splits=len(df_core_expand), shuffle=False, random_state=2017)




'''
------------------------------------------------------------
SVM
------------------------------------------------------------
'''
#%%
#--Setting up
#Data splitting and provide empty bottles
dfs = kf.split(df_core_expand)
precisions = []
recalls    = []
f1s        = []
labels_real = np.empty(shape=(0,0))
labels_predicted = np.empty(shape=(0,0))


#--Train all models
for train, test in dfs:
    df_train = df_core_expand.loc[train]
    df_test = df_core_expand.loc[test]

    #Initialize and train the model
    clf = sklearn.svm.SVC(kernel='linear', probability=False)
    clf.fit(df_train.filter(regex='[0-9]+', axis=1), df_train['group'])
    labels = clf.predict(df_test.filter(regex='[0-9]+', axis=1))

    #Evaluation
    precisions.append(sklearn.metrics.precision_score(df_test['group'], labels, average = 'weighted'))
    recalls.append(sklearn.metrics.recall_score(df_test['group'], labels, average = 'weighted'))
    f1s.append(sklearn.metrics.f1_score(df_test['group'], labels, average = 'weighted'))

    #Record true and predicted labels
    labels_real = np.append(labels_real, np.array(df_test['group']))
    labels_predicted = np.append(labels_predicted, labels)


#%%
#--Evaluate all models
#Indicators
print('precision: ' + str(np.mean(precisions)))
print('recall: ' + str(np.mean(recalls)))
print('f1 measure: ' + str(np.mean(f1s)))

#%%
#Confusion matrix
mat = confusion_matrix(labels_real, labels_predicted)
seaborn.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
                xticklabels=np.arange(1, numOfCluster + 1),
                yticklabels=np.arange(1, numOfCluster + 1))
plt.title('Confusion Matrix - SVM')
plt.xlabel('true label')
plt.ylabel('predicted label')
plt.savefig(r'..\img\test\2-2t_confusion_SVM_' + str(numOfCluster) + '_k' + str(keyGNum))
# plt.show()
plt.close()




'''
------------------------------------------------------------
Neural Nets (Multi-layer Perceptron (MLP))
------------------------------------------------------------
'''
#%%
#--Setting up
#Data splitting and provide empty bottles
dfs = kf.split(df_core_expand)
precisions = []
recalls    = []
f1s        = []
labels_real = np.empty(shape=(0,0))
labels_predicted = np.empty(shape=(0,0))


#--Train all models
for train, test in dfs:
    df_train = df_core_expand.loc[train]
    df_test = df_core_expand.loc[test]

    #Initialize and train the model
    clf = MLPClassifier()
    clf.fit(df_train.filter(regex='[0-9]+', axis=1), df_train['group'])
    labels = clf.predict(df_test.filter(regex='[0-9]+', axis=1))

    #Evaluation
    precisions.append(sklearn.metrics.precision_score(df_test['group'], labels, average = 'weighted'))
    recalls.append(sklearn.metrics.recall_score(df_test['group'], labels, average = 'weighted'))
    f1s.append(sklearn.metrics.f1_score(df_test['group'], labels, average = 'weighted'))

    #Record true and predicted labels
    labels_real = np.append(labels_real, np.array(df_test['group']))
    labels_predicted = np.append(labels_predicted, labels)


#%%
#--Evaluate all models
#Indicators
print('precision: ' + str(np.mean(precisions)))
print('recall: ' + str(np.mean(recalls)))
print('f1 measure: ' + str(np.mean(f1s)))

#%%
#Confusion matrix
mat = confusion_matrix(labels_real, labels_predicted)
seaborn.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
                xticklabels=np.arange(1, numOfCluster + 1),
                yticklabels=np.arange(1, numOfCluster + 1))
plt.title('Confusion Matrix - Neural Nets (MLP)')
plt.xlabel('true label')
plt.ylabel('predicted label')
plt.savefig(r'..\img\test\2-2t_confusion_NN_' + str(numOfCluster) + '_k' + str(keyGNum))
# plt.show()
plt.close()




'''
------------------------------------------------------------
Random forest (Apply bagging to improve decision trees)
------------------------------------------------------------
'''
#%%
#--Setting up
#Data splitting and provide empty bottles
dfs = kf.split(df_core_expand)
precisions = []
recalls    = []
f1s        = []
labels_real = np.empty(shape=(0,0))
labels_predicted = np.empty(shape=(0,0))


#--Train all models
for train, test in dfs:
    df_train = df_core_expand.loc[train]
    df_test = df_core_expand.loc[test]

    #Create an instance of our decision tree classifier.
    tree = DecisionTreeClassifier(max_depth=10)

    #Each tree uses up to 80% of the data
    clf = BaggingClassifier(tree, n_estimators=100, max_samples=0.8, random_state=1)

    #Fit the bagged classifier and visualize
    clf.fit(df_train.filter(regex='[0-9]+', axis=1), df_train['group'])
    labels = clf.predict(df_test.filter(regex='[0-9]+', axis=1))

    #Evaluation
    precisions.append(sklearn.metrics.precision_score(df_test['group'], labels, average = 'weighted'))
    recalls.append(sklearn.metrics.recall_score(df_test['group'], labels, average = 'weighted'))
    f1s.append(sklearn.metrics.f1_score(df_test['group'], labels, average = 'weighted'))

    #Record true and predicted labels
    labels_real = np.append(labels_real, np.array(df_test['group']))
    labels_predicted = np.append(labels_predicted, labels)


#%%
#--Evaluate all models
#Indicators
print('precision: ' + str(np.mean(precisions)))
print('recall: ' + str(np.mean(recalls)))
print('f1 measure: ' + str(np.mean(f1s)))

#%%
#Confusion matrix
mat = confusion_matrix(labels_real, labels_predicted)
seaborn.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
                xticklabels=np.arange(1, numOfCluster + 1),
                yticklabels=np.arange(1, numOfCluster + 1))
plt.title('Confusion Matrix - Random Forest')
plt.xlabel('true label')
plt.ylabel('predicted label')
plt.savefig(r'..\img\test\2-2t_confusion_RF_' + str(numOfCluster) + '_k' + str(keyGNum))
# plt.show()
plt.close()




'''
------------------------------------------------------------
Naive Bayes (multinomial)
------------------------------------------------------------
'''
#%%
#--Setting up
#Data splitting and provide empty bottles
dfs = kf.split(df_core_expand)
precisions = []
recalls    = []
f1s        = []
labels_real = np.empty(shape=(0,0))
labels_predicted = np.empty(shape=(0,0))


#%%
#--Train all models
for train, test in dfs:
    df_train = df_core_expand.loc[train]
    df_test = df_core_expand.loc[test]

    #Initialize and train the model
    clf = MultinomialNB()
    clf.fit(df_train.filter(regex='[0-9]+', axis=1) - np.min(df_train.filter(regex='[0-9]+', axis=1)), df_train['group'])
    labels = clf.predict(df_test.filter(regex='[0-9]+', axis=1))

    #Evaluation
    precisions.append(sklearn.metrics.precision_score(df_test['group'], labels, average = 'weighted'))
    recalls.append(sklearn.metrics.recall_score(df_test['group'], labels, average = 'weighted'))
    f1s.append(sklearn.metrics.f1_score(df_test['group'], labels, average = 'weighted'))

    #Record true and predicted labels
    labels_real = np.append(labels_real, np.array(df_test['group']))
    labels_predicted = np.append(labels_predicted, labels)


#%%
#--Evaluate all models
#Indicators
print('precision: ' + str(np.mean(precisions)))
print('recall: ' + str(np.mean(recalls)))
print('f1 measure: ' + str(np.mean(f1s)))

#%%
#Confusion matrix
mat = confusion_matrix(labels_real, labels_predicted)
seaborn.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
                xticklabels=np.arange(1, numOfCluster + 1),
                yticklabels=np.arange(1, numOfCluster + 1))
plt.title('Confusion Matrix - Multinomial Naive Bayes')
plt.xlabel('true label')
plt.ylabel('predicted label')
plt.savefig(r'..\img\test\2-2t_confusion_NB_' + str(numOfCluster) + '_k' + str(keyGNum))
# plt.show()
plt.close()
