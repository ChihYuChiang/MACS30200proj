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
count = True
keywordGroup = False
keyword = False


#%%
#--Read in data
df = pd.read_csv(r'..\data\output\df_predicted_all_doc2vec.csv', encoding='utf-8')
numOfCluster = len(df['Predicted'].unique())

df_raw = pd.read_csv(r'..\data\df_cb_main_expand25.csv', encoding='utf-8', error_bad_lines=False).dropna(subset=['Review']).drop_duplicates(['Author Name', 'Game Title'])
df_raw.shape

df_keygroup = pd.read_csv(r'..\data\output\df_predicted_doc2vec.csv', encoding='utf-8')

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
Count - normalized + wordcloud
------------------------------------------------------------
'''
#%%
if count:
    #--Normalize
    groupReview_normalized = []
    freqs = []
    for text in groupReview:
        tokens = nltk.word_tokenize(text)
        normalized = normlizeTokens(tokens, stopwordLst=stop_words_nltk, stemmer=snowball, lemmer=wordnet)
        freq = nltk.FreqDist(normalized)

        groupReview_normalized.append(normalized)
        freqs.append(freq)


    #%%
    #--Wordcloud
    #Exclude last 250 words
    excludeTop = 250
    for i in np.arange(len(freqs)):
        x = pd.DataFrame(freqs[i], index=np.arange(len(freqs[i])))
        y = pd.DataFrame(x.iloc[0]).sort_values(0)[:-excludeTop]

        z = []
        for w, f in y.itertuples():
            z.append((w, f))

        wc = wordcloud.WordCloud(background_color="white", max_words=200, max_font_size=200, width= 1500, height=1500, mode ='RGBA', scale=.5, ).fit_words(z)
        plt.imshow(wc)
        plt.axis("off")
        plt.savefig(r'..\img\2-4_highFreqWords_group' + str(i + 1) + '_exclude' + str(excludeTop))
        plt.show()
        plt.close()




'''
------------------------------------------------------------
Keyword Group Scores
------------------------------------------------------------
'''
#%%
if keywordGroup:
    df_keygroupScore = pd.merge(df_keygroup, df.filter(['Id', 'Predicted']), on='Id', how='left')
    df_keygroupScores = df_keygroupScore.groupby(by=['Predicted_x']).mean().filter(regex='^group\d+$')
    df_keygroupScores.to_csv(r'..\data\output\df_keygroupScores.csv',  encoding='utf-8')




'''
------------------------------------------------------------
Keyword Count
------------------------------------------------------------
'''
#%%
if keyword:
    #--Normalize and count with only keywords
    groupReview_normalized = []
    freqs = []
    for text in groupReview:
        tokens = nltk.word_tokenize(text)
        normalized = normlizeTokens(tokens, stopwordLst=stop_words_nltk, vocab=keyWords)
        freq = nltk.FreqDist(normalized)

        groupReview_normalized.append(normalized)
        freqs.append(freq)


    #%%
    #--Top words and wordcloud
    #Exclude last 125 words
    excludeTop = 125
    for i in np.arange(len(freqs)):
        x = pd.DataFrame(freqs[i], index=np.arange(len(freqs[i])))
        y = pd.DataFrame(x.iloc[0]).sort_values(0)[:-excludeTop]

        #Print the top words
        print('Most frequent keywords of group {}:'.format(i + 1))
        print(y[-30:])

        #Create wordclouds
        z = []
        for w, f in y.itertuples():
            z.append((w, f))
        
        wc = wordcloud.WordCloud(background_color="white", max_words=200, max_font_size=200, width= 1500, height=1500, mode ='RGBA', scale=.5, ).fit_words(z)
        plt.imshow(wc)
        plt.axis("off")
        plt.savefig(r'..\img\2-4_highFreqKeyWords_group' + str(i + 1) + '_exclude' + str(excludeTop))
        plt.show()
        plt.close()