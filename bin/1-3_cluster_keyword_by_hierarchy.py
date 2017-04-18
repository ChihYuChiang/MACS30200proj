#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

import scipy.spatial.distance as spsd
import scipy.cluster as scluster
import sklearn.decomposition
import sklearn.manifold


#%%
#--Read in data
keyWords, keyWordSubMatrix = pickle.load(open(r'..\data\process\keywordVecs.p', 'rb'))


keyWordSubMatrix
#%%
#--Compute cosine distance matrix
distMatrix = spsd.squareform(spsd.pdist(keyWordSubMatrix, metric='cosine'))


#%%
#--Ward clustering
#Return is in a special form, refer to scipy ilinkage matrix
linkageMatrix = scluster.hierarchy.ward(distMatrix)


#%%
#--Plot the hierarchical clustering tree_after a number of branch
#Put this in dendrogram: p=numBranches
numBranches = 5
plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
ax = scluster.hierarchy.dendrogram(linkageMatrix, truncate_mode='level', leaf_rotation=90, leaf_font_size=8, p=numBranches)
plt.savefig(r'..\img\1-3_ward_' + str(numBranches) + 'branch')
plt.show()
plt.close()


#%%
#--Designate the number of clusters
#This gives us an array giving each element of linkageMatrix's cluster
numClusters = 9
hierarchicalClusters = scluster.hierarchy.fcluster(linkageMatrix, numClusters, 'maxclust')
df_cluster = pd.DataFrame({
    'cluster': hierarchicalClusters,
    'keyword': keyWords
})

#Save for later use
df_cluster.to_csv(r'..\data\output\keywordGroup_hierarchy.csv', index=False)

#Observe
print("Titles per cluster:")
for i in range(numClusters):
    titles = df_cluster.query('cluster == @i + 1')[ :20]
    print("Cluster {}:".format(i))
    print(titles)


#%%
#--Reduce dimension
#Use PCA to reduce the dimesions to 50, and T-SNE to project them down to the two we will visualize.
#This is nondeterministic process, and so you can repeat and achieve alternative projectsions/visualizations of the words.
pcaWords = sklearn.decomposition.PCA(n_components=50).fit(keyWordSubMatrix)
reducedPCA_data = pcaWords.transform(keyWordSubMatrix)

#Further reduce to 2 by TSNE
#T-SNE is theoretically better, but you should experiment
tsneWords = sklearn.manifold.TSNE(n_components=2).fit_transform(reducedPCA_data)


#%%
#--Prepare for plot
#Find the coordinates of those words in your biplot
x = tsneWords[:, 0]
y = tsneWords[:, 1]

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
#--Visualize
#Color map for predicted labels (PCA)
colors_p = [colordict[l-1] for l in hierarchicalClusters]
fig = plt.figure(figsize = (10,6))
ax = fig.add_subplot(111)
ax.set_frame_on(False)
plt.scatter(x, y, color = colors_p, alpha = 0.5)
for i, word in enumerate(keyWords):
    ax.annotate(word, (x[i],y[i]))
plt.xticks(())
plt.yticks(())
plt.title('Predicted Clusters\n k = {}'.format(numClusters))
plt.savefig(r'..\img\1-3_ward_tsne_' + str(numClusters))
plt.show()