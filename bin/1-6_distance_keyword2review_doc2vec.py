#%%
import pandas as pd
import pickle
import numpy as np

import gensim
import sklearn.metrics


#%%
#--Read in data
D2V_WOstop = gensim.models.Doc2Vec.load(r'..\data\process\D2V_WOstop')
df = pd.read_csv(r'..\data\df_cb_main.csv', encoding='utf-8', error_bad_lines=False).drop_duplicates(subset='Game Title').dropna(subset=['Review'])
df_keyword_flat = pd.read_csv(r'..\data\output\keywordGroup_flat.csv', encoding='utf-8')
df_keyword_hier = pd.read_csv(r'..\data\output\keywordGroup_hierarchy.csv', encoding='utf-8')

#Choose to use flat
df_keyword = df_keyword_flat

#Acquire feature and key word lists
D2VFeatures = D2V_WOstop.vocab.keys()


#%%
#--Make into keyword groups
numOfGroup = len(df_keyword.group_label.unique())
keyWords = []
for g in range(numOfGroup):
    key = df_keyword.query('group_label == @g + 1').keyword.tolist()
    keyWords.append(key)

keyGroups = {
    'groupNo': np.arange(numOfGroup) + 1,
    'keyWords': keyWords,
    'keyWords_filtered': None,
    'centroid': None
}

df_keyGroups = pd.DataFrame(keyGroups)


keyWords_filtered = []
centroids = []
for index, row in df_keyGroups.iterrows():
    #Remove key words outside the D2V space
    filtered = [w for w in row['keyWords'] if w in D2VFeatures]
    keyWords_filtered.append(filtered)

    #Compute centroid vector of each group
    centroid = np.mean(D2V_WOstop[filtered], axis=0)
    centroids.append(centroid)

df_keyGroups['keyWords_filtered'] = keyWords_filtered
df_keyGroups['centroid'] = centroids

pickle.dump(df_keyGroups, open(r'..\data\process\df_keywordGroup_flatCentroid.p', 'wb'))


#%%
#--Acquire score of each key word group
#By the average distance of the docvec and each key word group
for g in range(len(df_keyGroups)):
    scores = []
    gvec = df_keyGroups['centroid'][g].reshape(1, -1)
    for index, row in df.iterrows():
        dvec = D2V_WOstop.docvecs[row['Game Title']].reshape(1, -1)
        score = sklearn.metrics.pairwise.cosine_similarity(gvec, dvec)[0, 0]

        scores.append(score)

    df['group' + str(g + 1)] = scores


#--Review and save
pickle.dump(df, open(r'..\data\process\score_original_doc2vec.p', 'wb'))
df[:10]
