#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

import gensim
import sklearn
import sklearn.decomposition
import sklearn.manifold
import scipy.spatial.distance as spsd
import scipy.cluster as scluster


#%%
#--Read in data
df_scores = pd.read_csv(r'..\data\process\tste\tste_embedding_25.csv', encoding='utf-8', header=None)

CORE_GAMES = pd.read_csv(r'..\data\raw_coregame\core_games.csv', encoding='utf-8', header=None)[0].tolist()
CORE_ID = pd.read_csv(r'..\data\raw_coregame\core_games.csv', encoding='utf-8', header=None)[1].tolist()


#%%
#--Compute cosine distance matrix
distMatrix = spsd.squareform(spsd.pdist(df_scores, metric='cosine'))


#%%
#--Ward clustering
#Return is in a special form, refer to scipy linkage matrix
linkageMatrix = scluster.hierarchy.ward(distMatrix)


#%%
#--Plot the hierarchical clustering tree
plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
ax = scluster.hierarchy.dendrogram(linkageMatrix, truncate_mode='level', leaf_rotation=90, leaf_font_size=8)
plt.savefig(r'..\img\2-1_ward')
plt.show()
plt.close()


#%%
#--Elbow method to detect proper cluster number
#Decide by the distance growth between clusters
last = linkageMatrix[-30:, 2]
last_rev = last[::-1]
idxs = np.arange(1, len(last) + 1)
plt.plot(idxs, last_rev)

acceleration = np.diff(last, 2)  # 2nd derivative of the distances
acceleration_rev = acceleration[::-1]
plt.plot(idxs[:-2] + 1, acceleration_rev)
plt.savefig(r'..\img\2-1_ward_elbow')
plt.show()
plt.close()

#%%
k = acceleration_rev.argmax() + 2  # if idx 0 is the max of this we want 2 clusters
print("clusters:", k)


#%%
#--Designate the number of clusters
numClusters = 7

#This gives us an array giving each element of linkageMatrix's cluster
def wardCluster(numClusters):
    hierarchicalClusters = scluster.hierarchy.fcluster(linkageMatrix, numClusters, 'maxclust')
    df_cluster = pd.DataFrame({
        'cluster': hierarchicalClusters,
        'game': CORE_GAMES
    })
    return df_cluster
wardCluster(numClusters)

#Observe
print("Titles per cluster:")
for i in range(numClusters):
    titles = wardCluster(numClusters).query('cluster == @i + 1')[ :20]
    print("Cluster {}:".format(i))
    print(titles)


#%%
#--Save cluster result for later
coreCluster = pd.DataFrame({
    'game_title': CORE_GAMES,
    'core_id': CORE_ID,
    'group_label': wardCluster(numClusters).cluster
    })
pickle.dump(coreCluster, open(r'..\data\process\core_cluster.p', 'wb'))


#%%
#--Prepare to plot
#Reduce dimension using the 2 dimension tste
tsteGames = pd.read_csv(r'..\data\process\tste\tste_embedding_2.csv', names=['x', 'y'], encoding='utf-8', header=None)

#Make color dictionery
colordict = {
0: 'red',
1: 'orange',
2: 'green',
3: 'blue',
4: 'c',
5: 'm',
6: 'y',
7: 'k',
8: 'bisque',
9: 'aquamarine',
10: 'blanchedalmond',
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


#%%
#--Color map for predicted labels (tste)
colors_p = [colordict[l] for l in km.labels_]
fig = plt.figure(figsize = (10,6))
ax = fig.add_subplot(111)
ax.set_frame_on(False)
plt.scatter(tsteGames.x, tsteGames.y, color = colors_p, alpha = 0.5)
for i, word in enumerate(CORE_GAMES):
    ax.annotate(word, (tsteGames.x[i],tsteGames.y[i]))
plt.xticks(())
plt.yticks(())
plt.title('Predicted Clusters\n k = {}'.format(numClusters))
plt.savefig(r'..\img\2-1_ward_tste2_' + str(numClusters))
plt.show()