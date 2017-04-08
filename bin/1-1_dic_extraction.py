#%%
#--Setting up
import re
import pandas as pd

#Read in dict file (113,632 words)
f = open(r"D:\OneDrive\GitHub\MACS30200proj\reference\Webster's Unabridged 09\29765-8.txt")
text = f.read()


#%%
#--Acquire keywords from each search term
#sens = sensation + sense
#perce = percept + perceive
terms = ['feel', 'emotion', 'experience', 'encounter', 'aware', 'mind', 'sens', 'state', 'perce', 'discover', 'view', 'interest', 'physic', 'mental', 'spiritual', 'concern', 'thought', 'concept', 'belie', 'rational', 'social', 'imagin'
]

regs = ['\n[^a-z]+\n.*?[' + term[0] + '|' + term[0].upper() + ']' + term[1:] for term in terms]
results = [re.findall(reg, text, re.DOTALL) for reg in regs]
words = [(re.findall('\n[^a-z]+\n', s)[-1]).strip() for result in results for s in result]
len(words)

#%%
#Remove duplicate
keywords = pd.Series(words).drop_duplicates()
len(keywords)

#%%
#Export
keywords.to_csv(r'..\data\process\keywords.csv', index=False)


#%%
#--Exploration
#Search specific term
term = 'cogniti'

reg = '\n[^a-z]+\n.*?[' + term[0] + '|' + term[0].upper() + ']' + term[1:]
results_ex = re.findall(reg, text, re.DOTALL)
result_ex = set([(re.findall('\n[^a-z]+\n', s)[-1]).strip() for s in results_ex])
print(result_ex)
print(len(result_ex))

#%%
#Search if specific keyword is in full result
key = 'ZOMBIE'

print(key in list(keywords))