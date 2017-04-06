#%%
import pandas as pd
import pickle
import numpy as np

import gensim


#%%
#--Load Google's pre-trained Word2Vec model.
model = gensim.models.Word2Vec.load_word2vec_format(r'..\reference\GoogleNews\GoogleNews-vectors-negative300.bin', binary=True)


#%%
#--Keywords
#Keywords pool
keyWords_raw = pd.read_csv(r'..\data\process\keywords.csv', encoding='utf-8', header=None)[0].tolist()

#Make lower-case
keyWords_raw = [word.lower() for word in keyWords_raw]
print(len(keyWords_raw))


#%%
#--Acquire key word submatrix (preserve the distances from the original)
keyWords = list(keyWords_raw)
keyWordSubMatrix = []
for word in keyWords_raw:
    try:
        keyWordSubMatrix.append(model[word])
    except:
        keyWords.remove(word)
        pass
keyWordSubMatrix = np.array(keyWordSubMatrix)
print(len(keyWords))

numKeyWord = keyWordSubMatrix.shape[0]
print(numKeyWord) #Some words can't be found in the original google space


#%%
#--Save
pickle.dump((keyWords, keyWordSubMatrix), open(r'..\data\process\keywordVecs.p', 'wb'))
