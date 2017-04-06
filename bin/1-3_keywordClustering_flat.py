#%%
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

import sklearn
import sklearn.decomposition
import sklearn.manifold
import sklearn.cluster


#%%
#--Read in data
keyWords, keyWordSubMatrix = pickle.load(open(r'..\data\process\keywordVecs.p', 'rb'))


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
#Plot
fig = plt.figure(figsize = (15, 10))
ax = fig.add_subplot(111)
ax.set_frame_on(False)
plt.scatter(tsneWords[:, 0], tsneWords[:, 1], alpha=1) #Making the points invisible
# for i, word in enumerate(keyWords):
#     ax.annotate(word, (tsneWords[:, 0][i],tsneWords[:, 1][i]))
plt.xticks(())
plt.yticks(())
plt.savefig(r'..\img\1-3_tsne')
plt.show()
plt.close()


#%%
#--K-mean flat clustering
#Setting up
numClusters = 9
randomState = 88
km = sklearn.cluster.KMeans(n_clusters=numClusters, init='random', random_state=randomState) #The result is changed according to the initial

#K-mean scores
kmScores = pd.DataFrame(km.fit_transform(keyWordSubMatrix), columns=['group_' + str(i + 1) for i in range(numClusters)])
kmScores = pd.merge(pd.DataFrame({
    'keyword': keyWords,
    'group_label': km.labels_ + 1
    }), kmScores, left_index=True, right_index=True)
kmScores

#Save for later use
kmScores.to_csv(r'..\data\output\keywordGroup_flat.csv', index=False)

#Top words
tops = []
print("Top words per cluster:")
for i in range(numClusters):
    top = kmScores.query('group_label == @i + 1').sort_values('group_' + str(i + 1))[-20: ]['keyword']
    tops.append(top)
    print("Cluster {}:".format(i))
    print(top)
tops = pd.concat(tops)


#%%
#--Prepare for visualization
#Reduce dimension by PCA
pca = sklearn.decomposition.PCA(n_components = 2).fit(keyWordSubMatrix)
reduced_data = pca.transform(keyWordSubMatrix)

#Find the coordinates of those words in your biplot
x = reduced_data[:, 0]
y = reduced_data[:, 1]

#Make a df
df_coor = pd.DataFrame({
    'keywords': keyWords,
    'x_pca': x,
    'y_pca': y,
    'x_tsne': tsneWords[:, 0],
    'y_tsne': tsneWords[:, 1]
})

df_top = df_coor[df_coor['keywords'].isin(tops)]

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
#--Color map for predicted labels
#plot n clusters (PCA)
colors_p = [colordict[l] for l in km.labels_]
fig = plt.figure(figsize = (10,6))
ax = fig.add_subplot(111)
ax.set_frame_on(False)
plt.scatter(x, y, color = colors_p, alpha = 0.5)
for i, row in df_top.iterrows():
    ax.annotate(row.keywords, (row.x_pca, row.y_pca))
plt.xticks(())
plt.yticks(())
plt.title('Predicted Clusters\n k = {}'.format(numClusters))
plt.savefig(r'..\img\1-3_k-mean_PCA_' + str(numClusters))
plt.show()

#plot n clusters (tsne)
colors_p = [colordict[l] for l in km.labels_]
fig = plt.figure(figsize = (10,6))
ax = fig.add_subplot(111)
ax.set_frame_on(False)
plt.scatter(tsneWords[:, 0], tsneWords[:, 1], color = colors_p, alpha = 0.5)
for i, row in df_top.iterrows():
    ax.annotate(row.keywords, (row.x_tsne, row.y_tsne))
plt.xticks(())
plt.yticks(())
plt.title('Predicted Clusters\n k = {}'.format(numClusters))
plt.savefig(r'..\img\1-3_k-mean_tsne_' + str(numClusters))
plt.show()


#%%
#--Selecting cluster number by silhouette method
range_n_clusters = np.arange(2,21)
X = keyWordSubMatrix
for n_clusters in range_n_clusters:
    # Create a subplot with 1 row and 2 columns
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18, 7)

    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    ax1.set_xlim([-0.1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

    # Initialize the clusterer with n_clusters value and a random generator
    # seed of 10 for reproducibility.
    clusterer = sklearn.cluster.KMeans(n_clusters=n_clusters, random_state=randomState)
    cluster_labels = clusterer.fit_predict(X)

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = sklearn.metrics.silhouette_score(X, cluster_labels)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    # Compute the silhouette scores for each sample
    sample_silhouette_values = sklearn.metrics.silhouette_samples(X, cluster_labels)

    y_lower = 10
    for i in range(n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = plt.cm.spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                            0, ith_cluster_silhouette_values,
                            facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    # 2nd Plot showing the actual clusters formed
    colors = plt.cm.spectral(cluster_labels.astype(float) / n_clusters)
    ax2.scatter(x, y, marker='.', s=30, lw=0, alpha=0.7,
                c=colors)

    # Labeling the clusters
    centers = clusterer.cluster_centers_
    projected_centers = pca.transform(centers)
    # Draw white circles at cluster centers
    ax2.scatter(projected_centers[:, 0], projected_centers[:, 1],
                marker='o', c="white", alpha=1, s=200)

    for i, c in enumerate(projected_centers):
        ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1, s=50)

    ax2.set_title("The visualization of the clustered data.")
    ax2.set_xlabel("PC 1")
    ax2.set_ylabel("PC 2")

    plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                    "with n_clusters = %d" % n_clusters),
                    fontsize=14, fontweight='bold')

    # plt.savefig(r'..\img\1-3_silhouette_' + str(n_clusters))
    # plt.show()
    plt.close()
