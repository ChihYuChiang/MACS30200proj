#%%
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

import gensim
import sklearn.decomposition
import sklearn.manifold
from sklearn.neural_network import MLPClassifier


#%%
#--Read in data
D2V_WOstop = gensim.models.Doc2Vec.load(r'..\data\process\D2V_WOstop')
df_core = pickle.load(open(r'..\data\process\core_cluster.p', 'rb'))
df = pickle.load(open(r'..\data\process\score_30_doc2vec.p', 'rb')) #df with distances from the last step


#%%
#--Acquire game vecs and separate into core and other games
core_idTags = []
core_groups = []

other_idTags = []
other_groups = []
other_titles = []

for index, row in df.iterrows():
    idTag = 'id_' + str(index)
    vec = D2V_WOstop.docvecs[idTag]
    title = row['Game']
    if row['CoreID'] > 0:
        group = (df_core[df_core['core_id'] == row['CoreID']])['group_label'].values[0]
        core_idTags.append(idTag)
        core_groups.append(group)
    elif row['CoreID'] == 0:
        other_idTags.append(idTag)
        other_titles.append(title)

core_vec = df.query('CoreID > 0').filter(regex=('^group\d+$'))
other_vec = df.query('CoreID == 0').filter(regex=('^group\d+$'))

numOfCluster = len(df_core.group_label.unique())


#%%
#--Dimension reduction for visualization
#Reduce dimension to 2 by PCA
pcaDocs = sklearn.decomposition.PCA(n_components=2).fit(np.vstack((core_vec, other_vec)))

reducedPCA = pcaDocs.transform(other_vec)

x_other = reducedPCA[:, 0]
y_other = reducedPCA[:, 1]

#Reduce dimension to 2 by TSNE
tsneGames = sklearn.manifold.TSNE(n_components=2).fit_transform(other_vec)

x_other_tsne = tsneGames[:, 0]
y_other_tsne = tsneGames[:, 1]


#%%
#--Initialize and train the model
clf = MLPClassifier()
clf.fit(core_vec, core_groups)
labels = clf.predict(other_vec)
labels.shape

#%%
#Save the predicted clusters
df_predicted = df.query('CoreID == 0').copy()
df_predicted['Predicted'] = labels
df_predicted.to_csv(r'..\data\output\df_predicted_keyG.csv', index=False, encoding='utf-8')

#%%
#Prepare games to be plotted
TARGET = pd.read_csv(r'..\data\target_for_elaborate.csv', encoding='utf-8', header=None)[0].tolist()
coor_target = []
coor_target_tsne = []
for game in TARGET:
    index = other_titles.index(game)
    coor_target.append(reducedPCA[index])
    coor_target_tsne.append(tsneGames[index])


#%%
#--Color map for predicted labels
#Make color dictionery
colordict = {
0: '#d53e4f',
1: '#f46d43',
2: '#fdae61',
3: '#ffffbf',
4: '#abdda4',
5: '#66c2a5',
6: '#3288bd',
7: '#fee08b',
8: '#88ddaa',
9: '#71acbc',
10: '#e6f598',
11: 'chartreuse',
12: 'cornsilk',
13: 'darkcyan',
14: 'darkkhaki',
15: 'forestgreen',
16: 'goldenrod',
17: 'lawngreen',
18: 'lightgray',
19: 'linen',
20: 'mediumorchid',
}

#Plot by PCA
colors_p = [colordict[l] for l in labels]
fig = plt.figure(figsize = (10,6))
ax = fig.add_subplot(111)
ax.set_frame_on(False)
plt.scatter(x_other, y_other, color = colors_p, alpha = 0.5)
for i, word in enumerate(TARGET):
    ax.annotate(word, (coor_target[i][0],coor_target[i][1]),
    horizontalalignment='center', alpha=0.7)
plt.xticks(())
plt.yticks(())
plt.title('All games with color representing predicted cluster\n classification: Neural Nets (MLP)\n k = {}, n = 15,372, projection = PCA'.format(numOfCluster))
plt.savefig(r'..\img\2-3-1_PCA_' + str(numOfCluster))
plt.show()
plt.close()

#Plot by tsne
colors_p = [colordict[l] for l in labels]
fig = plt.figure(figsize = (10,6))
ax = fig.add_subplot(111)
ax.set_frame_on(False)
plt.scatter(x_other_tsne, y_other_tsne, color = colors_p, alpha = 0.5)
# for i, word in enumerate(TARGET):
#     ax.annotate(word, (coor_target_tsne[i][0],coor_target_tsne[i][1]),
#     horizontalalignment='center', alpha=0.7)
plt.xticks(())
plt.yticks(())
plt.title('All games with color representing predicted cluster\n classification: Neural Nets (MLP) with 30-cluster input\n k = {}, n = 15,372, projection = tsne'.format(numOfCluster))
plt.savefig(r'..\img\2-3-1_tsne_' + str(numOfCluster))
plt.show()
plt.close()
