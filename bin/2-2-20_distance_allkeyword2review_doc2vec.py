#%%
import pandas as pd
import pickle
import numpy as np

import gensim
import sklearn.metrics


#%%
#--Read in data
D2V_WOstop = gensim.models.Doc2Vec.load(r'..\data\process\D2V_WOstop')
df = pd.read_csv(r'..\data\df_cb_main_expand25.csv', encoding='utf-8', error_bad_lines=False).dropna(subset=['Review']).drop_duplicates(['Author Name', 'Game Title'])
df_keyword_flat = pd.read_csv(r'..\data\output\keywordGroup_flat.csv', encoding='utf-8')
df_keyword_hier = pd.read_csv(r'..\data\output\keywordGroup_hierarchy.csv', encoding='utf-8')

#Choose to use flat
df_keyword = df_keyword_flat

#Acquire feature and key word lists
D2VFeatures = D2V_WOstop.vocab.keys()
df_keyword_filtered = df_keyword[df_keyword['keyword'].isin(D2VFeatures)]


#%%
#--Acquire score of each key word as feature
for i, k in enumerate(df_keyword_filtered['keyword']):
    scores = []
    kvec = D2V_WOstop[k].reshape(1, -1)
    for index, row in df.iterrows():
        dvec = D2V_WOstop.docvecs['id_' + str(row['Id'])].reshape(1, -1)
        score = sklearn.metrics.pairwise.cosine_similarity(kvec, dvec)[0, 0]

        scores.append(score)

    df['f_' + str(i + 1)] = scores


#--Review and save
pickle.dump(df, open(r'..\data\process\score_new_all_doc2vec.p', 'wb'))
df.query('Core > 0')
