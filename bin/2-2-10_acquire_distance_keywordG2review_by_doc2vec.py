#%%
import pandas as pd
import pickle
import numpy as np

import gensim
import sklearn.metrics


#%%
#--Read in data
D2V_WOstop = gensim.models.Doc2Vec.load(r'..\data\process\D2V_WOstop')
df = pd.read_csv(r'..\data\df_cb_main_combined.csv', index_col=0, encoding='utf-8', error_bad_lines=False).dropna(subset=['Review']).drop_duplicates(['Author', 'Game'])

#Acquire feature and key word lists
D2VFeatures = D2V_WOstop.vocab.keys()

#Setup target keyword group cluster
numOfGroups = [10, 30, 100, 300, 1000]


#%%
for n in numOfGroups:
    numOfGroup = n
    #--Read in corresponding keyword group file
    df_keyword = pd.read_csv(r'..\data\output\keywordGroup_hierarchy_' + str(numOfGroup) + '.csv', encoding='utf-8')


    #--Make into keyword groups
    keyWords = []
    for g in range(numOfGroup):
        key = df_keyword.query('cluster == @g + 1').keyword.tolist()
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
        try: centroid = np.mean(D2V_WOstop[filtered], axis=0)
        except: centroid = None
        centroids.append(centroid)

    df_keyGroups['keyWords_filtered'] = keyWords_filtered
    df_keyGroups['centroid'] = centroids

    #Leave only non-null groups
    df_keyGroups = df_keyGroups[pd.notnull(df_keyGroups['centroid'])]


    #%%
    #--Acquire score of each key word group
    #By the average distance of the docvec and each key word group
    for g in range(len(df_keyGroups)):
        scores = []
        try:
            gvec = df_keyGroups['centroid'][g].reshape(1, -1)
            for index, row in df.iterrows():
                dvec = D2V_WOstop.docvecs['id_' + str(index)].reshape(1, -1)
                score = sklearn.metrics.pairwise.cosine_similarity(gvec, dvec)[0, 0]

                scores.append(score)

            df['group' + str(g + 1)] = scores
        #Some groups contain to word
        except: pass


    #--Review and save
    pickle.dump(df, open(r'..\data\process\score_' + str(numOfGroup) + '_doc2vec.p', 'wb'))
    df.query('CoreID > 0')


#--Print top games of each keygroup
#Also the score must be the highest among all scores of the game to be chosen
if False:
    CORE_GAMES = pd.read_csv(r'..\data\core_games.csv', encoding='utf-8', header=None)[0].tolist()
    for i in np.arange(numOfGroup) + 1:
        print('Games with top scores in group' + str(i))
        maxScore = df[df['group' + str(i)] == np.max(df.filter(regex='^group\d+$'), axis=1)]
        topScoreGames = df.sort_values(by='group' + str(i))[:100]
        top_notcore = topScoreGames[topScoreGames.Core == 0]['Game']
        print(top_notcore)