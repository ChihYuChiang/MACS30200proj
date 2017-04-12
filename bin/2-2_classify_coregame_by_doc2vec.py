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


#%%
#--Read in data
#Remember to expand the review
D2V_WOstop = gensim.models.Doc2Vec.load(r'..\data\process\D2V_WOstop')
df = pd.read_csv(r'..\data\df_cb_main_expand25.csv', encoding='utf-8', error_bad_lines=False).dropna(subset=['Review']).drop_duplicates(['Author Name', 'Game Title'])
df_core = pickle.load(open(r'..\data\process\core_cluster.p', 'rb'))


#%%
#--Core game vecs
idTags = []
groups = []
coreVecs = []
for index, row in df.iterrows():
    if row['Core'] > 0:
        idTag = 'id_' + str(row['Id'])
        group = (df_core[df_core['core_id'] == row['Core']])['group_label'].values[0]
        vec = D2V_WOstop.docvecs[idTag]

        idTags.append(idTag)
        groups.append(group)
        coreVecs.append(vec)

coreVecs = np.array(coreVecs)


#%%
#--Dimension reduction for visualization by PCA
pcaDocs = sklearn.decomposition.PCA(n_components = 2).fit(coreVecs)
reducedPCA = pcaDocs.transform(coreVecs)
print(reducedPCA.shape)


#%%
#--Organize into a df except vecs
df_core_expand = pd.DataFrame({
    'idTag': idTags,
    'group': groups,
    'pca1': reducedPCA[:, 0],
    'pca2': reducedPCA[:, 1]
})
numOfCluster = len(df_core_expand.group.unique())

#Randomize for testing
df_core_expand = df_core_expand.sample(frac=1, random_state=210)


#%%
#--Split data (70% training, 30% testing)
cut_point   = round(0.7 * len(df_core_expand))

df_train = df_core_expand[ :cut_point]
df_test  = df_core_expand[cut_point: ]

vect_train  = coreVecs[ :cut_point]
vect_test   = coreVecs[cut_point: ]




'''
------------------------------------------------------------
SVM
------------------------------------------------------------
'''
#%%
#--Initialize and train the model
clf = sklearn.svm.SVC(kernel='linear', probability=False)
clf.fit(vect_train, df_train['group'])
labels = clf.predict(vect_test)


#%%
#--Evaluation
#Confusion matrix
mat = confusion_matrix(df_test['group'], labels)
seaborn.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
                xticklabels=np.arange(1, numOfCluster + 1),
                yticklabels=np.arange(1, numOfCluster + 1))
plt.title('Confusion Matrix - SVM')
plt.xlabel('true label')
plt.ylabel('predicted label')
plt.savefig(r'..\img\2-2_confusion_SVM_' + str(numOfCluster))
plt.show()
plt.close()

print(sklearn.metrics.precision_score(df_test['group'], labels, average = 'weighted')) #precision
print(sklearn.metrics.recall_score(df_test['group'], labels, average = 'weighted')) #recall
print(sklearn.metrics.f1_score(df_test['group'], labels, average = 'weighted')) #F-1 measure




'''
------------------------------------------------------------
Neural Nets (Multi-layer Perceptron (MLP))
------------------------------------------------------------
'''
#%%
#--Initialize and train the model
clf = MLPClassifier()
clf.fit(vect_train, df_train['group'])
labels = clf.predict(vect_test)


#%%
#--Evaluation
#Confusion matrix
mat = confusion_matrix(df_test['group'], labels)
seaborn.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
                xticklabels=np.arange(1, numOfCluster + 1),
                yticklabels=np.arange(1, numOfCluster + 1))
plt.title('Confusion Matrix - Neural Nets (MLP)')
plt.xlabel('true label')
plt.ylabel('predicted label')
plt.savefig(r'..\img\2-2_confusion_NN_' + str(numOfCluster))
plt.show()
plt.close()

print(sklearn.metrics.precision_score(df_test['group'], labels, average = 'weighted')) #precision
print(sklearn.metrics.recall_score(df_test['group'], labels, average = 'weighted')) #recall
print(sklearn.metrics.f1_score(df_test['group'], labels, average = 'weighted')) #F-1 measure




'''
------------------------------------------------------------
Random forest (Apply bagging to improve decision trees)
------------------------------------------------------------
'''
#%%
#--Setting up
#Create an instance of our decision tree classifier.
tree = DecisionTreeClassifier(max_depth=10)

#Each tree uses up to 80% of the data
bag = BaggingClassifier(tree, n_estimators=100, max_samples=0.8, random_state=1)


#%%
#--Fit the bagged classifier and visualize
bag.fit(vect_train, df_train['group'])
labels = bag.predict(vect_test)


#%%
#--Evaluation
#Confusion matrix
mat = confusion_matrix(df_test['group'], labels)
seaborn.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
                xticklabels=np.arange(1, numOfCluster + 1),
                yticklabels=np.arange(1, numOfCluster + 1))
plt.title('Confusion Matrix - Random Forest')
plt.xlabel('true label')
plt.ylabel('predicted label')
plt.savefig(r'..\img\2-2_confusion_RF_' + str(numOfCluster))
plt.show()
plt.close()

print(sklearn.metrics.precision_score(df_test['group'], labels, average = 'weighted')) #precision
print(sklearn.metrics.recall_score(df_test['group'], labels, average = 'weighted')) #recall
print(sklearn.metrics.f1_score(df_test['group'], labels, average = 'weighted')) #F-1 measure




'''
------------------------------------------------------------
Naive Bayes (multinomial)
------------------------------------------------------------
'''
#%%
model = MultinomialNB()
model.fit((vect_train - np.min(vect_train)), df_train['group'])
labels = model.predict((vect_test - np.min(vect_train)))

#%%
#--Evaluation
#Confusion matrix
mat = confusion_matrix(df_test['group'], labels)
seaborn.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
                xticklabels=np.arange(1, numOfCluster + 1),
                yticklabels=np.arange(1, numOfCluster + 1))
plt.title('Confusion Matrix - Multinomial Naive Bayes')
plt.xlabel('true label')
plt.ylabel('predicted label')
plt.savefig(r'..\img\2-2_confusion_NB_' + str(numOfCluster))
plt.show()
plt.close()

print(sklearn.metrics.precision_score(df_test['group'], labels, average = 'weighted')) #precision
print(sklearn.metrics.recall_score(df_test['group'], labels, average = 'weighted')) #recall
print(sklearn.metrics.f1_score(df_test['group'], labels, average = 'weighted')) #F-1 measure
