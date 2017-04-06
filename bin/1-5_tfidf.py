#%%
import pandas as pd
import numpy as np
import pickle

import sklearn.feature_extraction


#%%
#--Read in data
df = pd.read_csv(r'..\data\df_cb_main.csv', encoding='utf-8', error_bad_lines=False).drop_duplicates(subset='Game Title').dropna(subset=['Review'])
print(len(df))


#%%
#--Filter for feature words and produce tf-idf
#To prune this matrix of features, we now limit our word vector to 3000 words with at most 50% doc occurrences and exist at least 2 times in all docs.
#initialize
tfidfVectorizer = sklearn.feature_extraction.text.TfidfVectorizer(max_df=0.5, min_df=10, max_features=3000, stop_words='english', norm='l2')

#train
tfidfVects = tfidfVectorizer.fit_transform(df['Review'])
pickle.dump((tfidfVectorizer, tfidfVects), open(r'..\data\process\tfidfVects.p', 'wb'))
print(tfidfVects)


#%%
#--Observe
try:
    print(tfidfVectorizer.vocabulary_['server'])
except KeyError:
    print('vector is missing')
    print('The available words are: {} ...'.format(list(tfidfVectorizer.vocabulary_.keys())[ :10]))
