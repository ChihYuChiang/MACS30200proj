#%%
import pandas as pd
import re
from nltk.corpus import wordnet as wn

#Keywords identified by dictionary inversed look-up
keywords = pd.read_csv(r'..\data\process\keywords.csv', encoding='utf-8', header=None)[0].tolist()


#%%
#--Function for acquiring lemmas in WordNet structure
def getRelevantWords(word):
    relevantWords = []
    syns = wn.synsets(word)

    #Aquire synsets: itself + hyper + hypo
    for syn in wn.synsets(word):
        syns = syns + syn.hypernyms() + syn.hyponyms()
    
    #Acquire lemmas: each synset + lemmas' anto + lemmas' pertain
    for syn in syns:
        words = [lemma.name() for lemma in syn.lemmas()]
        antoWords = [lemma.name() for word in syn.lemmas() for lemma in word.antonyms()]
        pertainWords = [lemma.name() for word in syn.lemmas() for lemma in word.pertainyms()]

        relevantWords = relevantWords + words + antoWords + pertainWords
    
    return relevantWords


#%%
#--Apply to each keyword
wordLists = map(getRelevantWords, keywords)

#Flatten list of lists
keywords_expand = [word for wordList in wordLists for word in wordList]

#Remove n-grams (linked with _)
temp = keywords_expand
keywords_expand = []
for word in temp:
    if not re.search('_', word): keywords_expand.append(word)

#Include original keywords and drop duplicates
keywords_expand = pd.Series(keywords_expand + keywords).drop_duplicates()


#%%
#--Examine and save
print(len(keywords_expand))
keywords_expand.to_csv(r'..\data\process\keywords_expand.csv', index=False)

