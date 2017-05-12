#%%
import pandas as pd
import pickle
import numpy as np

import gensim


#%%
#--Read in data
W2V_WOstop = gensim.models.Word2Vec.load(r'..\data\process\W2V_WOstop')
tfidfVectorizer, tfidfVects = pickle.load(open(r'..\data\process\tfidfVects.p', 'rb'))
df = pd.read_csv(r'..\data\df_cb_main.csv', encoding='utf-8', error_bad_lines=False).drop_duplicates(subset='Game Title').dropna(subset=['Review'])
df_keyword_flat = pd.read_csv(r'..\data\output\keywordGroup_flat.csv', encoding='utf-8')
df_keyword_hier = pd.read_csv(r'..\data\output\keywordGroup_hierarchy.csv', encoding='utf-8')

#Choose to use flat
df_keyword = df_keyword_flat

#Acquire feature and key word lists
W2VFeatures = W2V_WOstop.vocab.keys()
tfidfFeatures = pd.Series(tfidfVectorizer.get_feature_names())

THRES_TFIDF = 0


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
    'keyWords_filtered': None
}

df_keyGroups = pd.DataFrame(keyGroups)

#Remove key words outside the W2V space
keyWords_filtered = []
for index, row in df_keyGroups.iterrows():
    keyWords_filtered.append([w for w in row['keyWords'] if w in W2VFeatures])
df_keyGroups['keyWords_filtered'] = keyWords_filtered


#%%
#--Acquire review feature words
reviewFeatureWords = []
for index in range(len(df)):
    #Acquire index and filter
    indexesAboveThreshold = [i for i in range(tfidfVects.shape[1]) if (tfidfVects[index])[0, i] > THRES_TFIDF]

    #Acquire feature words by index
    reviewFeatureWord = list(tfidfFeatures[indexesAboveThreshold])

    #Remove features outside the W2V space
    reviewFeatureWord_filtered = [w for w in reviewFeatureWord if w in W2VFeatures]

    reviewFeatureWords.append(reviewFeatureWord_filtered)

df['reviewFeatureWord'] = reviewFeatureWords


#%%
#--Acquire score of each key word group
#By the average distance of the feature words and each key word group
for g in range(len(df_keyGroups)):
    scores = []
    for index in range(len(df)):
        score = W2V_WOstop.n_similarity(df_keyGroups['keyWords_filtered'][0], reviewFeatureWords[index])

        scores.append(score)

    df['group' + str(g + 1)] = scores


#--Review and save
pickle.dump(df, open(r'..\data\process\score_original_tfidfWords.p', 'wb'))
df[:10]
