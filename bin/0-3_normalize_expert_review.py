#%%
import pandas as pd
import pickle

import nltk
import gensim


#%%
#--Read in data
df = pd.read_csv(r'..\data\df_cb_main_combined.csv', index_col=0, encoding='utf-8', error_bad_lines=False).dropna(subset=['Review']).drop_duplicates(['Author', 'Game'])
print(len(df.query('CoreID > 0')))


#%%
#--Normalization
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

#%%
#Normalization
df['Review_tokenized_sent'] = df['Review'].astype('str').apply(lambda x: [nltk.word_tokenize(s) for s in nltk.sent_tokenize(x)])
df['Review_normalized_sent_Wstop'] = df['Review_tokenized_sent'].apply(lambda x: [normlizeTokens(s) for s in x])
df['Review_normalized_sent_WOstop'] = df['Review_tokenized_sent'].apply(lambda x: [normlizeTokens(s, stopwordLst = stop_words_nltk) for s in x])

df['Review_tokenized_arti'] = df['Review'].astype('str').apply(lambda x: nltk.word_tokenize(x))
df['Review_normalized_arti_WOstop'] = df['Review_tokenized_arti'].apply(lambda x: normlizeTokens(x, stopwordLst = stop_words_nltk))
pickle.dump(df, open(r'..\data\process\df_normalized.p', 'wb'))
