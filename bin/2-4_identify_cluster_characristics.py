#%%
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import re

import wordcloud
import nltk
from nltk.corpus import stopwords
import sklearn.feature_extraction
import sklearn.manifold

#%%
#--Switches (use only one True a time)
tfidf = False
count = False
keywordGroup = False
keyword = True
numOfCluster = 7

#%%
#--Read in data
df = pd.read_csv(r'..\data\output\df_predicted.csv', encoding='utf-8')
numOfCluster = len(df['Predicted'].unique())

df_raw = pd.read_csv(r'..\data\df_cb_main_combined.csv', index_col=0, encoding='utf-8', error_bad_lines=False).dropna(subset=['Review']).drop_duplicates(['Author', 'Game'])
df_raw.shape

df_keygroup = pd.read_csv(r'..\data\output\df_predicted_keyG.csv', encoding='utf-8')

keyWords, keyWordSubMatrix = pickle.load(open(r'..\data\process\keywordVecs.p', 'rb'))
print(len(keyWords))


#%%
#--Create text groups by label (cluster)
groupReview = [[] for i in range(numOfCluster)]
for i in range(numOfCluster):
    groupReview[i] = df.query('Predicted == @i + 1').Review.values.sum()
len(groupReview)


#%%
#--Normalization for counting
#Function for normalization
def normlizeTokens(tokenLst, stopwordLst=None, stemmer=None, lemmer=None, vocab=None):
    #We can use a generator here as we just need to iterate over it
    #Lowering the case and removing non-words
    workingIter = (w.lower() for w in tokenLst if w.isalpha())
    #Now we can use the stemmer, if provided
    if stemmer is not None:
        workingIter = (stemmer.stem(w) for w in workingIter)
    #And the lemmer
    if lemmer is not None:
        workingIter = (lemmer.lemmatize(w) for w in workingIter)
    #And remove the stopwords
    if stopwordLst is not None:
        workingIter = (w for w in workingIter if w not in stopwordLst)
    #We will return a list with the stopwords removed
    if vocab is not None:
        vocab_str = '|'.join(vocab)
        workingIter = (w for w in workingIter if re.match(vocab_str, w))
    return list(workingIter)

#Initialize our stemmer and our stop words
stop_words_nltk = nltk.corpus.stopwords.words('english')
snowball = nltk.stem.snowball.SnowballStemmer('english')
wordnet = nltk.stem.WordNetLemmatizer()




'''
------------------------------------------------------------
Tfidf
------------------------------------------------------------
'''
#%%
if tfidf:
    #%%
    #--Filter for feature words and produce tf-idf
    tfidfVectorizer = sklearn.feature_extraction.text.TfidfVectorizer(max_df=0.4,  max_features=1000, stop_words='english', norm='l2')

    #train
    tfidfVects = tfidfVectorizer.fit_transform(groupReview)
    pickle.dump((tfidfVectorizer, tfidfVects), open(r'..\data\process\tfidfVects_bycluster.p', 'wb'))
    tfidfVects.shape


    #%%
    #--Observe
    try:
        print(tfidfVectorizer.vocabulary_['dota'])
    except KeyError:
        print('vector is missing')
        print('The available words are: {} ...'.format(list(tfidfVectorizer.vocabulary_.keys())[ :10]))

    features = pd.Series(tfidfVectorizer.get_feature_names())


    #%%
    #--Acquire top 50 words of each cluster
    groupFeature = [[] for i in range(numOfCluster)]
    for i in range(numOfCluster):
        keys = np.argsort(tfidfVects[i].todense()).tolist()[0][-50:]
        groupFeature[i] = features.iloc[keys]

    print(groupFeature)




'''
------------------------------------------------------------
Keyword Group Scores
------------------------------------------------------------
'''
#%%
if keywordGroup:
    df_keygroupScore = pd.merge(df_keygroup, df.filter(['Predicted']), left_index=True, right_index=True)
    df_keygroupScores = df_keygroupScore.groupby(by=['Predicted_x']).mean().filter(regex='^group\d+$')
    df_keygroupScores.to_csv(r'..\data\output\df_keygroupScores.csv',  encoding='utf-8')
