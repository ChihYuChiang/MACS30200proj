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
game_titles = []
for index, row in df.iterrows():
    if row['CoreID'] > 0:
        idTag = 'id_' + str(index)
        group = (df_core[df_core['core_id'] == row['CoreID']])['group_label'].values[0]
        game_title = row['Game']

        idTags.append(idTag)
        groups.append(group)
        game_titles.append(game_title)


#%%
#--Get core game vecs and organize into a df
#The first "group" is coregame cluster tag; "groupn" is the distance between each doc and keyword group centroid
df_core_expand = pd.DataFrame({
    'idTag': idTags,
    'group': groups,
    'game_title': game_titles
})


'''
Turn genre info into dummy vars, as the predictors
************************************************************
************************************************************
'''
#Specify columns to be renamed (can also do index)
df_tGenre = pd.read_csv('..\data\df_cb_genre.csv').rename(columns={'Unnamed: 0': 'Id'})

df_tGenre = df_tGenre.groupby(by=['Game Title', 'Genre']).count().unstack(fill_value=0)
df_tGenre.columns = df_tGenre.columns.droplevel(0)
df_tGenre.where(cond=lambda x = df_tGenre: x == 0, other=1, inplace=True)

#Make into a df
df_core_expand = pd.merge(df_core_expand, df_tGenre,                          left_on='game_title', right_index=True).drop_duplicates(subset='game_title')
df_core_expand.iloc[:, 3:]
numOfCluster = len(df_core_expand.group.unique())

#Save for later
df_core_expand.to_csv(r'..\data\process\traditional_genre.csv')
'''
************************************************************
************************************************************
'''




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
    df_train = df_core_expand.iloc[train]
    df_test = df_core_expand.iloc[test]

    #Initialize and train the model
    clf = sklearn.svm.SVC(kernel='linear', probability=False)
    clf.fit(df_train.iloc[:, 3:], df_train['group'])
    labels = clf.predict(df_test.iloc[:, 3:])

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
    df_train = df_core_expand.iloc[train]
    df_test = df_core_expand.iloc[test]

    #Initialize and train the model
    clf = MLPClassifier()
    clf.fit(df_train.iloc[:, 3:], df_train['group'])
    labels = clf.predict(df_test.iloc[:, 3:])

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
    df_train = df_core_expand.iloc[train]
    df_test = df_core_expand.iloc[test]

    #Create an instance of our decision tree classifier.
    tree = DecisionTreeClassifier(max_depth=10)

    #Each tree uses up to 80% of the data
    clf = BaggingClassifier(tree, n_estimators=100, max_samples=0.8, random_state=1)

    #Fit the bagged classifier and visualize
    clf.fit(df_train.iloc[:, 3:], df_train['group'])
    labels = clf.predict(df_test.iloc[:, 3:])

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
    df_train = df_core_expand.iloc[train]
    df_test = df_core_expand.iloc[test]

    #Initialize and train the model
    clf = MultinomialNB()
    clf.fit(df_train.iloc[:, 3:] - np.min(df_train.iloc[:, 3:]), df_train['group'])
    labels = clf.predict(df_test.iloc[:, 3:])

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
